'''
A runner to run the analysis directly on remotes using
'''

import os
from newsrods.sparkrods import run


def main():
    '''
    Link the file loading with the query
    '''

    run(os.environ['SGE_TASK_ID'])


if __name__ == "__main__":
    main()
