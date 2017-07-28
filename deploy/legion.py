'''
Fabric definitions for running on Legion
'''

from fabric.api import task, env, execute
from deploy.remote import set_vars


@task
def legion(username):
    '''
    Set up the machine name and hosts for Legion
    '''
    env.hosts = ['legion.rc.ucl.ac.uk']
    env.machine = 'legion'
    execute(set_vars, username=username)
