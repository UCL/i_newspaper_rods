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

def mapper(issue):
    matching_articles = 0
    all_articles = 0
    for article in issue.articles:
        all_articles +=1
        cword=None
        for word in article.words:
            preceding=cword
            cword=word
            if word in interesting_words:
                matching_articles+=1
                break
            if word in interesting_twograms_dict.keys():
                if preceding == interesting_twograms_dict[word]:
                    matching_articles+=1
                    break


    return {issue.date.year: [1, all_articles, matching_articles]}

reducer=merge_under(triple_sum)
