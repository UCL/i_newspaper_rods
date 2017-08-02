'''
Set up to run locally. This is designed to be used for testing
'''

from fabric.api import task, env, execute, lcd, local


@task
def setup(query, datafile, number_oid=-1):
    '''
    Prepare instance for running. Generates necessary files and installs
    packages
    '''
    execute(dependencies)
    execute(install, query=query, datafile=datafile)
    execute(storeids, number=number_oid)


@task
def install(query, datafile):
    '''
    Run the tests
    '''
    env.results_dir = 'results'
    local('mkdir -p ' + env.results_dir)
    with lcd(env.results_dir):  # pylint: disable=not-context-manager
        local('cp -r ../newsrods .')
        local('cp ../' + query + ' ./newsrods/query.py')
        local('cp ../' + datafile + ' .')


@task
def test():
    '''
    Run the query on the sub set of files
    '''
    with lcd(env.results_dir):  # pylint: disable=not-context-manager
        local('pyspark < newsrods/local_runner.py')


@task
def storeids(number):
    '''
    Get the oids for the archive. However, since this is just a local
    test which is unable to process large amounts of files, save only
    a small subset.

    If the number is less than 1 return the full set
    '''
    head_command = ''""''
    if number > 0:
        head_command = ' | head -n ' + str(number)
    lib_path = "''"
    try:
        lib_path = env.DYLD_LIBRARY_PATH
    except KeyError:
        pass
    with lcd(env.results_dir):  # pylint: disable=not-context-manager
        local('DYLD_LIBRARY_PATH=' + lib_path + ' iinit', shell='/bin/bash')
        local('DYLD_LIBRARY_PATH=' + lib_path + ' iquest --no-page "%s" ' +
              '"SELECT DATA_PATH where COLL_NAME like ' +
              "'" + env.corpus + "%'" +
              " and DATA_NAME like '%-%.xml' " +
              " and DATA_RESC_HIER = 'wos;wosArchive'" + '"' + head_command +
              ' > oids.txt', shell='/bin/bash')


@task
def dependencies():
    '''
    Install the dependencies
    '''
    local('. venv/bin/activate && pip install lxml pyyaml pytest psutil')


@task
def pytest():
    '''
    Run the pytest tests
    '''
    local('py.test')
