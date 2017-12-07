'''
This module looks for regex matches in articles. It returns the full matching
expression for each match. This can be used to find the context in which a word
occurs. Note that this should probbably be limited to local context (a few
words).
'''

from operator import add
import re
from yaml import load


def do_query(issues, get_input):
    '''
    Get the text which matches a given regex in an issue.
    '''
    # Get the list of words to search for
    with open(get_input(1)) as words_file:
        words = list(words_file)
    with open(get_input(2)) as rules_file:
        match_rules = load(rules_file)
    context_words = str(match_rules['context_words'])
    word_regex = match_rules['word_regex'].strip()
    context_regex = r"(?:" + word_regex + r"\s*){," + \
                    context_words + r"}"
    print(context_regex)
    interesting_words = [re.compile(context_regex + r'\b' + word.strip() +
                                    r'\b' + context_regex, re.I | re.U)
                         for word in words]
    print([m.pattern for m in interesting_words])
    # Map each article in each issue to a year of publication
    articles = issues.flatMap(lambda issue: [(issue.date.year, article) for
                                             article in issue.articles])
    # Add 1 record for each word that appears in each article in each year
    interest = articles.flatMap(lambda (year, article):
                                [((year, regex.pattern),
                                  regex.findall(article.words_string)) for
                                 regex in interesting_words])
    # Now add sum the year-word counts, and change the format for output
    interesting_by_year = interest \
        .flatMap(lambda (year_pat, matches): [((year_pat[0], year_pat[1],
                                                match.lower()), 1)
                                              for match in matches]) \
        .reduceByKey(add) \
        .map(lambda (year_pat_match, count): (year_pat_match[0],
                                              (year_pat_match[1],
                                               year_pat_match[2],
                                               count))) \
        .groupByKey() \
        .map(lambda (year, data): (year, list(data))) \
        .collect()
    return interesting_by_year
