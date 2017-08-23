'''
A runner to run the analysis directly on remotes using
'''

from newsrods.sparkrods import get_streams
from newsrods.query import do_query  # noqa # pylint: disable=all

from pyspark import SparkContext  # pylint: disable=import-error
import yaml


def main():
    '''
    Link the file loading with the query
    '''

    context = SparkContext(appName="iNewspaperRods")
    issues = get_streams(context, source="oids.1.txt")
    results = do_query(issues, 'input.1.data')

    with open('result.1.yml', 'w') as result_file:
        result_file.write(yaml.safe_dump(dict(results)))


if __name__ == "__main__":
    main()
