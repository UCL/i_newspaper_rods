'''
Fabric definitions for running on Grace
'''

from fabric.api import task, env


@task
def grace():
    '''
    Set up the machine name and hosts for Grace
    '''
    env.hosts = ['grace.rc.ucl.ac.uk']
    env.machine = 'grace'
