'''
A runner to run the analysis directly using pyspark. This must be run that
way as it relies on the REPL's SparkContext (sc).
'''

from newsrods.sparkrods import get_streams
from newsrods.query import do_query  # pylint: disable=all

from yaml import safe_dump


def main():
    '''
    Link the file loading with the query
    '''
    issues = get_streams(sc)  # noqa # pylint: disable=undefined-name
    result = do_query(issues, 'interesting_gender_words.txt')
    with open('result.yml', 'w') as result_file:
        result_file.write(safe_dump(dict(result)))


if __name__ == "__main__":
    main()
