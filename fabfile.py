from deploy.remote import *
from deploy.grace import grace

env.user='ucgajhe'

env.results_dir="/home/"+env.user+"/Scratch/TDASpark2/output"

env.model="newsrods"
env.corpus='/rdZone/live/rd009s/2TB-Drive-Transfer-06-07-q2016/TDA_GDA_1785-2009'

env.deploy_to="/home/"+env.user+"/devel/TDA"
env.clone_url="git@github.com:UCL/i_newspaper_rods.git"
