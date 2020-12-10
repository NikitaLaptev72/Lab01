import pandas
import re
import csv
import dateutil.parser
import datetime

DataFrame = pandas.read_csv("Vacancies.csv", delimiter = ",", index_col = [0], na_values = ['NA'], low_memory = False)

delimiters = ['/','+',' ']

comb = ['c++','c#','php','asp.net','ui','ux','qt','sql','delphi','vuejs','angular','unix','linux','java','typescript','win','kotlin','golang','python','node.js','backend','frontend','junior', 'middle', 'senior','go','html5','html','reactjs','ios','android']

variants = [
        ['frontend', 'front-end', 'front end', 'фронтенд', 'фронтэндер'],
        ['backend', 'back-end', 'back end', 'бэкенд'],
        ['developer', 'разработчик'],
        ['programmer', 'программист'],
        ['game designer', 'гейм дизайнер', 'геймдизайнер'],
        ['designer', 'дизайнер'],
        ['copywriter', 'копирайтер'],
        ['manager', 'менеджер'],
        ['animator', 'аниматор'],
        ['artist', 'художник'],
        ['middle','миддл'],
        ['js', 'javascript'],
        ['web','вэб'],
        ['teamlead','тимлид', 'team lead', 'team leader'],
        ['devops', 'девопс'],
        ['fullstack','full стек','full-стек','full stack'],
        ['бд','баз данных','баз даных','базы данных'],
        ['2d','2д'],
        ['3d','3д'],
        ['bitrix','битрикс'],
        ['analyst','аналитик'],
        ['big data','bigdata'],
        ['tech lead','techlead'],
        ['mssql','ms sql'],
        ['presale','pre sale', 'presales', 'pre sales']
    ]

Del = ['удаленно','remote','full-time','full time','фултайм','fulltime', '(\(.*\))','(\[.*\])','\s+в\s+.*','г\.\s+.*']

DataFrame["Name"] = DataFrame["Name"].apply(lambda x: x.lower())
DataFrame["Name"] = DataFrame["Name"].apply(lambda x: x.replace('\\','/'))
DataFrame["Name"] = DataFrame["Name"].apply(lambda x: x.replace('|','/'))
DataFrame["Name"] = DataFrame["Name"].apply(lambda x: x.replace(',','/'))
DataFrame["Name"] = DataFrame["Name"].apply(lambda x: x.replace('-',' '))
DataFrame["Name"] = DataFrame["Name"].apply(lambda x: re.sub('\s*\/\s*', '/', x))
DataFrame["Name"] = DataFrame["Name"].apply(lambda x: re.sub('\s+', ' ', x).strip())

for d in Del:
    regex = re.compile(d)
    DataFrame["Name"] = DataFrame["Name"].apply(lambda x: regex.sub('', x))

for v in variants:
    for i in range(1, len(v)):
        DataFrame["Name"] = DataFrame["Name"].apply(lambda x: x.replace(v[i],v[0]))

for i in range(len(comb)):
    for j in range(i+1, len(comb)):
        for d in delimiters:
            regex = re.compile(re.escape(comb[j])+'\s*'+re.escape(d)+'\s*'+re.escape(comb[i]))
            DataFrame["Name"] = DataFrame["Name"].apply(lambda x: regex.sub(comb[i]+delimiters[0]+comb[j], x))

DataFrame["Name"] = DataFrame["Name"].apply(lambda x: re.sub('\s+', ' ', x).strip())

DataFrame["Employer name"] = DataFrame["Employer name"].fillna("Не указано")
DataFrame["City"] = DataFrame["City"].fillna("Не указан")
DataFrame["Expierence"] = DataFrame["Expierence"].fillna("Не требуется")
DataFrame["Employment"] = DataFrame["Employment"].fillna("Любой тип")
DataFrame["Schedule"] = DataFrame["Schedule"].fillna("Любой график")
DataFrame["Responsibility"] = DataFrame["Responsibility"].fillna("Нету")
DataFrame["Requirement"] = DataFrame["Requirement"].fillna("Нету")
DataFrame["Key skills"] = DataFrame["Key skills"].fillna("Нету")

DataFrame["Salary from"] = DataFrame.groupby(["Name", "City"]).transform(lambda x: x.fillna(x.mean()))["Salary from"]
DataFrame["Salary to"] = DataFrame.groupby(["Name", "City"]).transform(lambda x: x.fillna(x.mean()))["Salary to"]

DataFrame["Published at"] = DataFrame["Published at"].apply(lambda x: (datetime.datetime.now() - dateutil.parser.parse(x).replace(tzinfo=None)).days)

DataFrame.to_csv("Result.csv",  na_rep = 'NA', index = True, index_label = "", quotechar = '"', quoting = csv.QUOTE_NONNUMERIC, encoding = "utf-8-sig")
