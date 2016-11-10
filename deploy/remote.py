from fabric.api import *
from mako.template import Template
import mako
import os
from datetime import datetime
from contextlib import nested

env.hosts=['legion.rc.ucl.ac.uk']
env.machine='legion'
env.user='ucgajhe'

@task
def sub(query, subsample=1, processes=12, wall='0:15:0'):
    env.processes=processes
    env.subsample=subsample

    env.wall=wall
    now=datetime.now()
    stamp=now.strftime("%Y%m%d_%H%M")
    outpath=os.path.basename(query).replace('.py','')+'_'+stamp

    template_file_path=os.path.join(os.path.dirname(__file__),
                                    env.machine+'.sh.mko')

    env.run_at = env.results_dir + '/'+outpath

    with open(template_file_path) as template:
        script=Template(template.read()).render(**env)
        with open('query.sh','w') as script_file:
            script_file.write(script)

    run('mkdir -p '+env.run_at)
    with cd(env.run_at):
       put(env.model, '.')
       put(query, 'query.py')
       put('query.sh','query.sh')
       run('cp ../oids.txt .')
       run('qsub query.sh')

@task
def storeids():
    run('mkdir -p '+env.results_dir)
    with cd(env.run_at):
       with prefix('module load icommands'):
           run('iinit')
           run('iquest --no-page "%s" '+
           '"SELECT DATA_PATH where COLL_NAME like '+
           "'"+env.corpus+"'"+
           " and DATA_NAME like '%-%.xml' "+
           " and DATA_RESC_HIER = 'wos;wosArchive'"+'" >oids.txt')

@task
def stat():
    run('qstat')

@task
def fetch():
    with lcd(os.path.join(os.path.dirname(os.path.dirname(__file__)),'results')):
      with cd(env.run_at):
        get('*')

@task
def dependencies():
    with modules:
        run("pip install --user lxml")
        run("pip install --user pyyaml")
        run("pip install --user pytest")
