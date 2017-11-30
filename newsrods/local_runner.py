'''
A runner to run the analysis directly on on the local machine
'''

from newsrods.sparkrods import run


def main():
    '''
    Link the file loading with the query
    '''
    run(str(1))


if __name__ == "__main__":
    main()
