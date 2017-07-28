'''
Set up to run locally. This is designed to be used for testing
'''

import os
from datetime import datetime
from fabric.api import task, env, execute, run, put, cd, prefix, lcd, local
from mako.template import Template


@task
def test_setup():
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
    local('mkdir -p ' + env.deploy_to)
    with lcd(env.deploy_to):
        put(env.model, '.')
        put('setup.py', 'setup.py')
        put('README.md', 'README.md')
        with prefix('module load python2/recommended'):
            run('python setup.py develop --user')
            run('py.test')


@task
def test(query, subsample=1, processes=12, wall='0:15:0'):
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
def dependencies():
    '''
    Install the dependencies
    '''
    local('. venv/bin/activate && pip install lxml pyyaml pytest')
