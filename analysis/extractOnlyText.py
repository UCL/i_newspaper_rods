'''
Collect text from XML fragments resulting from whitechapel queries
'''

from lxml import etree  # pylint: disable=all
import yaml


FILENAMES = ['./result.' + str(number) + '.yml' for number in range(1, 46)]

i = 1
for fname in FILENAMES:
    texts = []
    stream = file(fname, 'r')
    batch_data = yaml.load(stream)
    for list_articles in batch_data.itervalues():
        for article in list_articles:
            parser = etree.XMLParser(recover=True)
            tree = etree.fromstring(article, parser)
            title = tree.xpath('text/text.title/p/wd/text()')
            preamble = tree.xpath('text/text.preamble/p/wd/text()')
            content = tree.xpath('text/text.cr/p/wd/text()')
            words = title + preamble + content
            words_string = ' '.join(words).replace(' - ', '')
            texts.append(words_string)
    with open('test/test.' + str(i) + '.yml', 'w') as output:
        output.write(yaml.dump(texts, default_flow_style=False))
        i += 1
    stream.close()
