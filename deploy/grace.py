'''
Fabric definitions for running on Grace
'''

from fabric.api import task, env, execute
from deploy.remote import set_vars


@task
def grace(username):
    '''
    Set up the machine name and hosts for Grace
    '''
    env.hosts = ['grace.rc.ucl.ac.uk']
    env.machine = 'grace'
    execute(set_vars, username=username)
