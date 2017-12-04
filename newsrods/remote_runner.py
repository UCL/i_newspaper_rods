'''
A runner to run the analysis directly on remotes using
'''

import os
from newsrods.sparkrods import run


if __name__ == "__main__":
    run(os.environ['SGE_TASK_ID'])
