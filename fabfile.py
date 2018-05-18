"""
Fab file for deployment
"""

from datetime import datetime
from io import SEEK_SET, StringIO
from os import environ, mkdir
from os.path import join
from re import match
from shutil import copy2, copytree, ignore_patterns, rmtree

from fabric import Connection

from invoke import Exit, task

from mako.template import Template

from pandas import read_csv


CORPUS_ROOT = '/mnt/gpfs/live/ritd-ag-project-rd00hn-raleg13/'
DATA_SERVER = 'live.rd.ucl.ac.uk'
LOCAL_DEPLOY_DIR = 'results'
OID_FILE = 'oids.txt'


@task
def run_local(conn, username, datafile, query, number=5):
    """
    Run the code locally to test
    """
    prepare(query, datafile)
    storeids(int(number), username)
    pytest(conn)
    pyspark_local(conn)


@task
def run_remote(conn, datafile, query, username, years_per_chunk,
               min_year=0, max_year=9e9, number=0):
    """
    Run the code on a remote server
    """
    prepare(query, datafile)
    storeids(int(number), username)
    last = breakup(int(years_per_chunk),
                   int(min_year),
                   int(max_year))
    run_at = make_target_dir(username)
    upload(conn, last, run_at)
    test_remote(conn, run_at)
    submit(conn, run_at)


def storeids(number, username):
    """
    Get the files for the archive. However, since this is potentially just a
    local test which is unable to process large amounts of files, save only
    a small subset.

    If the number is less than 1 return the full set
    """
    connection = Connection(host=DATA_SERVER, user=username)
    head_command = ''
    if int(number) > 0:
        head_command = ' | head -n ' + str(number)
    indata = StringIO()
    errdata = StringIO()
    data = connection.run('find {} -name "*.xml" {}'.
                          format(CORPUS_ROOT, head_command),
                          echo=False, err_stream=errdata,
                          out_stream=indata)
    if data.return_code != 0:
        print('Error in retrieving list of oids')
        errdata.seek(SEEK_SET)
        print(errdata.read())
        Exit(-1)
    indata.seek(SEEK_SET)
    with open(join(LOCAL_DEPLOY_DIR, OID_FILE), 'w') as oid_file:
        while True:
            line = indata.readline()
            if not line:
                break
            oid_file.write(line)
    connection.close()


def prepare(query, datafile):
    """
    Move all the files to the run directory
    """
    rmtree(LOCAL_DEPLOY_DIR, ignore_errors=True)
    mkdir(LOCAL_DEPLOY_DIR)
    copytree('newsrods', join(LOCAL_DEPLOY_DIR, 'newsrods'),
             ignore=ignore_patterns('*.pyc', '__pycache__'))
    copy2(query, join(LOCAL_DEPLOY_DIR, 'newsrods/query.py'))
    copy2(datafile, join(LOCAL_DEPLOY_DIR, 'input.1.data'))
    copy2('requirements.txt', join(LOCAL_DEPLOY_DIR, 'requirements.txt'))


def pytest(conn):
    """
    Run the pytest tests
    """
    conn.run('cd results && py.test', shell='/bin/bash', env=environ)


def breakup(years_per_chunk, min_year, max_year):
    """
    Break up the input based on the year of output
    """
    print('Pruning years with min year', min_year, 'and max year', max_year)
    all_files = read_csv(join(LOCAL_DEPLOY_DIR, OID_FILE),
                         header=None, names=['Path'])
    all_files = all_files.assign(Year=all_files.
                                 Path.
                                 map(lambda path:
                                     int(filter(is_year, path.split('/')).
                                         __next__())))
    all_files = all_files[(all_files.Year >= min_year) &
                          (all_files.Year <= max_year)]
    all_files = all_files.assign(YearChunk=all_files.
                                 Year.map(lambda year:
                                          int(year / years_per_chunk)))
    all_files = all_files.assign(FileIndex=all_files.YearChunk -
                                 all_files.YearChunk.min() + 1)
    last = 0
    for group_id, subtable in all_files.groupby('FileIndex'):
        subtable.reset_index(drop=True).Path.to_csv(join(LOCAL_DEPLOY_DIR,
                                                         'oids.') +
                                                    str(group_id) +
                                                    '.txt', header=False,
                                                    index=False)
        last = max(int(last), group_id)
    return last


def is_year(part):
    """
    Return true if this string looks like a year
    """
    if len(part) != 4:
        return False
    return match(r'^\d*$', part)


def make_target_dir(username):
    """
    Declare the variables for where to store things on the cluster nodes
    """
    now = datetime.now()
    stamp = now.strftime('%Y%m%d_%H%M')

    results_dir = '/home/{}/Scratch/TDASpark'.format(username)
    run_at = '{}/{}'.format(results_dir, stamp)
    return run_at


def upload(conn, last, run_at, machine='legion', wall='10:0:0'):
    """
    Upload the code to the remote server
    """
    # Generate script for qsub
    template_file_path = join('deploy', '{}.sh.mko'.format(machine))
    env = {'wall': wall,
           'run_at': run_at,
           'last': last}

    with open(template_file_path) as template:
        script = Template(template.read()).render(**env)
        with open(LOCAL_DEPLOY_DIR + '/query.sh', 'w') as script_file:
            script_file.write(script)

    conn.run('mkdir -p {}'.format(run_at))
    archive_name = 'newsrods.tar.gz'
    conn.local('cd results && tar czvf {} .'.format(archive_name))
    conn.put(join(LOCAL_DEPLOY_DIR, archive_name), join(run_at, archive_name))
    conn.run('cd {} && tar -xzvf {}'.format(run_at, archive_name))


def test_remote(conn, run_at):
    """
    Set up any necessary libraries and run pytest to make sure it works
    """
    conn.run('module load python3/recommended && '
             'cd {} && '
             'pip install --user -r requirements.txt && '
             'py.test'.format(run_at), echo=True)


def submit(conn, run_at):
    """
    Submit the job to the cluster queue
    """
    conn.run('cd {} && qsub query.sh'.format(run_at))


@task
def pyspark_local(conn):
    """
    Run the query on the sub set of files
    """
    conn.run('cd {} && PYSPARK_PYTHON=python3 '
             'pyspark < newsrods/local_runner.py'.format(LOCAL_DEPLOY_DIR),
             env=environ)
