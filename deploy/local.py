"""
Set up to run locally. This is designed to be used for testing
"""

import os

from fabric.api import env, execute, lcd, local, task

import pandas as pd


@task
def setup(query, datafile, username, years_per_chunk=1e10, number_oid=-1):
    """
    Prepare instance for running. Generates necessary files and installs
    packages
    """
    execute(install, query=query, datafile=datafile)
    execute(storeids, number=number_oid, username=username)
    execute(breakup, years_per_chunk=int(years_per_chunk))


@task
def install(query, datafile):
    """
    Run the tests
    """
    local('rm -rf ' + env.local_deploy_dir)
    local('mkdir -p ' + env.local_deploy_dir)
    with lcd(env.local_deploy_dir):  # pylint: disable=not-context-manager
        local('cp -r ../newsrods .')
        local('cp ../' + query + ' ./newsrods/query.py')
        local('cp ../' + datafile + ' input.1.data')
        local('find . -iname "*.pyc" -delete')
        local('find . -iname "__pycache__" -delete')


@task
def test():
    """
    Run the query on the sub set of files
    """
    with lcd(env.local_deploy_dir):  # pylint: disable=not-context-manager
        local('pyspark < newsrods/local_runner.py')


@task
def storeids(number, username):
    """
    Get the files for the archive. However, since this is just a local
    test which is unable to process large amounts of files, save only
    a small subset.

    If the number is less than 1 return the full set
    """
    head_command = ''
    if int(number) > 0:
        head_command = ' | head -n ' + str(number)
    with lcd(env.local_deploy_dir):  # pylint: disable=not-context-manager
        local('ssh {}@{} find {} -name "*.xml" {} > oids.txt'.format(
            username, env.server, env.corpus, head_command),
              shell='/bin/bash')


@task
def pytest():
    """
    Run the pytest tests
    """
    local('py.test')


@task
def breakup(years_per_chunk):
    """
    Break up the input based on the year of output
    """
    all_files = pd.read_csv(os.path.join(env.local_deploy_dir, "oids.txt"),
                            header=None, names=['Path', 'OID'])
    all_files = all_files.assign(Year=all_files.Path.map(lambda path:
                                                         int(path[1:5])))
    all_files = all_files.assign(YearChunk=all_files.
                                 Year.map(lambda year:
                                          int(year / years_per_chunk)))
    all_files = all_files.assign(FileIndex=all_files.YearChunk -
                                 all_files.YearChunk.min() + 1)
    env.last = 0
    for group_id, subtable in all_files.groupby('FileIndex'):
        subtable.reset_index(drop=True).OID.to_csv(os.path.
                                                   join(env.local_deploy_dir,
                                                        "oids.") +
                                                   str(group_id) +
                                                   ".txt", header=False,
                                                   index=False)
        env.last = max(int(env.last), group_id)
