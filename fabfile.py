'''
Fab file for deployment
'''

from deploy.remote import env, prepare, stat, sub, fetch  # noqa # pylint: disable=unused-import
from deploy.grace import grace  # noqa # pylint: disable=unused-import
from deploy.legion import legion  # noqa # pylint: disable=unused-import
from deploy.local import setup, test, pytest  # noqa # pylint: disable=unused-import

env.local_deploy_dir = 'results'
env.model = "newsrods"
env.corpus = '/rdZone/live/rd009s/2TB-Drive-Transfer-06-07-q2016/' \
             + 'TDA_GDA_1785-2009'
