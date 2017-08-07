'''
Set up to run on Legion
'''

import os
from datetime import datetime
from fabric.api import task, env, execute, run, put, cd, prefix, lcd, get
from mako.template import Template


@task
def prepare():
    '''
    Prepare instance for running. Generates necessary files and installs
    packages
    '''
    execute(install)
    execute(dependencies)


@task
def set_vars(username):
    '''
    Declare the variables for where to store things on the cluster nodes
    '''
    now = datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M")

    results_dir = "/home/" + username + "/Scratch/TDASpark"
    env.run_at = results_dir + '/' + stamp

    env.user = username


@task
def install():
    '''
    Run the python setuptools code
    '''
    run('mkdir -p ' + env.run_at)
    with cd(env.run_at):  # pylint: disable=not-context-manager
        put(env.local_deploy_dir + '/*', '.')
        put('setup.py', 'setup.py')
        put('README.md', 'README.md')
        put('deploy/sparkrun', 'sparkrun')
        put('deploy/*.sh', '.')
        run('zip -r news.zip newsrods')


@task
def sub(processes=12, wall='2:0:0'):
    '''
    Submit task to the HPC job queue
    '''
    env.processes = processes
    env.wall = wall

    template_file_path = os.path.join(os.path.dirname(__file__),
                                      env.machine + '.sh.mko')

    with lcd(env.local_deploy_dir):  # pylint: disable=not-context-manager
        with open(template_file_path) as template:
            script = Template(template.read()).render(**env)
            with open('query.sh', 'w') as script_file:
                script_file.write(script)

        with cd(env.run_at):  # pylint: disable=not-context-manager
            put('query.sh', 'query.sh')
            run('qsub query.sh')


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
    # pylint: disable=not-context-manager
    with lcd(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                          'results')):
        with cd(env.run_at):  # pylint: disable=not-context-manager
            get('*')


@task
def dependencies():
    '''
    Install the dependencies
    '''
    # pylint: disable=not-context-manager
    with prefix('module load python2/recommended'):
        run("pip install --user lxml pyyaml pytest psutil requests")
        run('py.test')
