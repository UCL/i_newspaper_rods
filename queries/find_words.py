interesting_words = ['Holland',
                         'Netherlands',
                         'Netherland',
                         'Flanders',
                         'Flemish',
                         'Frisian',
                         'Friesland',
                         'Frisia',
                         'Belgium',
                         'Belgian',
                         'Wallonia',
                         'Amsterdam',
                         'Rotterdam',
                         'Utrecht',
                         'Groningen',
                         'Leeuwarden',
                         'Zwolle',
                         'Deventer',
                         'Tilburg',
                         'Overijssel',
                         'Drenthe',
                         'Gelderland',
                         'Guelders',
                         'Gelders',
                         'Twente',
                         'Twenthe',
                         'Drente',
                         'Drenthe',
                         'Brabant',
                         'Brabantian',
                         'Limburg',
                         'Limburgian',
                         'Limbourg',
                         'Limbourgian',
                         'Zeeland',
                         'Zeeuws',
                         'Sealand',
                         'Zeelandic',
                         'Sealandic',
                         'North-Holland',
                         'Noord-Holland',
                         'South-Holland',
                         'Zuid-Holland',
                         'Texel',
                         'Ameland',
                         'Schiermonnikoog',
                         'Vlieland',
                         'Batavia',
                         'Batavian',
                         'Indies',
                         'Suriname',
                         'Curacao',
                         'Aruba',
                         'Almere',
                         'Lelystad',
                         'Hindeloopen',
                         'Almeloo',
                         'Hengelo',
                         'Roermond',
                         'Breda',
                         'Tilburg',
                         'Willemstad',
                         'Amersfoort',
                         'Bruges',
                         'Brugge',
                         'Gent',
                         'Ghent',
                         'Bruxelles',
                         'Brussel',
                         'Brussels',
                         'Antwerp',
                         'Anvers',
                         'Antwerpen',
                         'Maline',
                         'Mechelen',
                         'Ypres',
                         'Ieper',
                         'Passchendaele',
                         'Pachendale',
                         'Vlissingen',
                         'Flushing',
                         'Middelburg',
                         'Zierikzee',
                         'Wallonian',
                         'Dutch',
                         'Flemish',
                         'Hollandic',
                         'Benelux',
                         'Luembourg',
                         'Luxemburg',
                         'Luxembourgian',
                         'Luxemburgian']

interesting_ngrams=[
            ['Low','Countries'],
            ['The','Hague'],
            ['Den','Haag'],
            ['East','Indies']
]

interesting_twograms_dict={
    x[1]:x[0] for x in interesting_ngrams
}

import collections

def mapper(issue):
    matching_articles = collections.defaultdict(int)
    all_articles = 0
    for article in issue.articles:
        all_articles +=1
        for word in interesting_words:
            if word in article.words:
                matching_articles[word]+=1

    return {issue.date.year: dict(matching_articles)}

reducer=merge_under(merge_under(sum))
