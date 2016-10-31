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

def q(issues, sc):
    # Ignoring 2-grams for now while trying out spark
    articles = issues.flatMap(lambda x: [(x.date, article) for article in x.articles])
    target_articles = articles.cartesian(sc.parallelize(interesting_words))
    interesting_articles = target_articles.filter(lambda x: x[1] in x[0][1].words)
    interesting_byyear = interesting_articles.map(
                                lambda x: ((x[0][0].year, x[1]), 1)).countByKey()
    # Now group on year first
    #interesting_by_year = sc.parallelize(interesting_by_both).map(
    #    lambda x: (x[0][0], (x[0][1], x[1]))).groupByKey().collect()
    return dict(interesting_by_year)
