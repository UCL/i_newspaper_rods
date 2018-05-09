"""
Fab file for deployment
"""

from deploy.grace import grace
from deploy.legion import legion
from deploy.local import pytest, setup, test
from deploy.remote import env, fetch, prepare, stat, sub

env.local_deploy_dir = 'results'
env.corpus = '/mnt/gpfs/live/ritd-ag-project-rd00hn-raleg13/'
env.server = 'live.rd.ucl.ac.uk'
