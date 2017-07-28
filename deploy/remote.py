'''
Set up to run on Legion
'''

import os
from datetime import datetime
from fabric.api import task, env, execute, run, put, cd, prefix, lcd, get
from mako.template import Template

env.hosts = ['legion.rc.ucl.ac.uk']
env.machine = 'legion'
env.user = 'ucgajhe'


@task
def prepare():
    '''
    Prepare instance for running. Generates necessary files and installs
    packages
    '''
    execute(dependencies)
    execute(install)
    execute(storeids)


@task
def install():
    '''
    Run the python setuptools code
    '''
    run('mkdir -p ' + env.deploy_to)
    with cd(env.deploy_to):
        put(env.model, '.')
        put('setup.py', 'setup.py')
        put('README.md', 'README.md')
        with prefix('module load python2/recommended'):
            run('python setup.py develop --user')
            run('py.test')


@task
def sub(query, subsample=1, processes=12, wall='0:15:0'):
    '''
    Submit task to the HPC job queue
    '''
    env.processes = processes
    env.subsample = subsample

    env.wall = wall
    now = datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M")
    outpath = os.path.basename(query).replace('.py', '') + '_' + stamp

    template_file_path = os.path.join(os.path.dirname(__file__),
                                      env.machine + '.sh.mko')

    env.run_at = env.results_dir + '/' + outpath

    with open(template_file_path) as template:
        script = Template(template.read()).render(**env)
        with open('query.sh', 'w') as script_file:
            script_file.write(script)

    run('mkdir -p ' + env.run_at)
    with cd(env.run_at):
        put(query, 'query.py')
        put('query.sh', 'query.sh')
        run('cp ../oids.txt .')
        run('qsub query.sh')


@task
def storeids():
    '''
    Get the oids for the archive
    '''
    run('mkdir -p ' + env.results_dir)
    with cd(env.results_dir):
        with prefix('module load icommands'):
            run('iinit')
            run('iquest --no-page "%s" ' +
                '"SELECT DATA_PATH where COLL_NAME like ' +
                "'" + env.corpus + "%'" +
                " and DATA_NAME like '%-%.xml' " +
                " and DATA_RESC_HIER = 'wos;wosArchive'" + '" >oids.txt')


@task
def stat():
    '''
    Get the status of the HPC queues
    '''
    run('qstat')


@task
def fetch():
    '''
    Copy the results back from the cluster
    '''
    with lcd(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          'results')):
        with cd(env.run_at):
            get('*')


@task
def dependencies():
    '''
    Install the dependencies
    '''
    with prefix('module load python2/recommended'):
        run("pip install --user lxml")
        run("pip install --user pyyaml")
        run("pip install --user pytest")
