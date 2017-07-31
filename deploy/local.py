'''
Set up to run locally. This is designed to be used for testing
'''

import os
from datetime import datetime
from fabric.api import task, env, execute, run, put, cd, lcd, local
from mako.template import Template


@task
def test_setup(number_oid=5):
    '''
    Prepare instance for running. Generates necessary files and installs
    packages
    '''
    execute(dependencies)
    execute(install)
    execute(storeids, number=number_oid)


@task
def install():
    '''
    Run the tests
    '''
    env.results_dir = 'results'
    local('py.test')


@task
def test(query):
    '''
    Run the query on the sub set of files
    '''
    local('mkdir -p ' + env.results_dir)
    with cd(env.run_at):
        put(query, 'query.py')
        put('query.sh', 'query.sh')
        run('cp ../oids.txt .')
        run('qsub query.sh')


@task
def storeids(number=5):
    '''
    Get the oids for the archive. However, since this is just a local
    test which is unable to process large amounts of files, save only
    a small subset.
    '''
    local('mkdir -p ' + env.results_dir)
    lib_path = "''"
    try:
        lib_path = env.DYLD_LIBRARY_PATH
    except KeyError:
        pass
    with lcd(env.results_dir):
        local('DYLD_LIBRARY_PATH=' + lib_path + ' iinit', shell='/bin/bash')
        local('DYLD_LIBRARY_PATH=' + lib_path + ' iquest --no-page "%s" ' +
              '"SELECT DATA_PATH where COLL_NAME like ' +
              "'" + env.corpus + "%'" +
              " and DATA_NAME like '%-%.xml' " +
              " and DATA_RESC_HIER = 'wos;wosArchive'" + '" | head -n ' +
              str(number) + ' > oids.txt', shell='/bin/bash')


@task
def dependencies():
    '''
    Install the dependencies
    '''
    local('. venv/bin/activate && pip install lxml pyyaml pytest requests')
