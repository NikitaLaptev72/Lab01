from lxml import etree
import pandas as pd
import numpy as np
import re

Data = []#Для записи в файл csv
Row = []
ColumnNames = []#массив заголовков

#Чтение XML
root = etree.parse("OBV_full.xml")

#Добавление заголовков столбцов
Vacancies = root.find('vacancies').getiterator('vacancy')
for Vacancy in Vacancies:
  tags = Vacancy.getiterator()
  for i in tags:
    if (i.tag not in ColumnNames):
      ColumnNames.append(i.tag)
  
#Для выпонения заданий    
ColumnNames.remove('address')
ColumnNames.remove('addresses')
ColumnNames.remove('salary')
ColumnNames.append('min_salary')
ColumnNames.append('max_salary')

columns = {}
for i in range(len(ColumnNames)):
    columns[ColumnNames[i]] = i

def Add_Row(row, column_name, value):
    index = columns[column_name]
    if not (pd.isna(row[index])):
        row[index] = row[index]+':'+value
    else:
        row[index] = value

#для записи максимальной и минимальной зарплаты
min_salary = re.compile("от: (\d+)", re.IGNORECASE)
max_salary = re.compile("до: (\d+)", re.IGNORECASE)

Vacancies = root.find('vacancies').getiterator('vacancy')

for vacancy in Vacancies:
    if (len(Row)!=0):
        Data.append(Row)
    Row = [np.nan] * len(ColumnNames)
    tags = vacancy.getiterator()
    for i in tags:
        if (i.text and not i.text.isspace() and i.tag!='vacancy' and i.tag!='address' and i.tag!='addresses'):
            if (i.tag == 'job-name'):
                Add_Row(Row, i.tag, i.text.replace(',',';'))
            elif (i.tag == 'salary'):
                min_s = min_salary.search(i.text)
                max_s = max_salary.search(i.text)
                min_s = min_s.group(1) if min_s else np.nan
                max_s = max_s.group(1) if max_s else np.nan
                Add_Row(Row, 'min_salary', min_s)
                Add_Row(Row, 'max_salary', max_s)
            else:
                Add_Row(Row, i.tag, i.text)
if Row:
    Data.append(Row)

#Запись данных в файл .csv
CSV = pd.DataFrame(Data, columns=ColumnNames)
CSV.to_csv("Result.csv",  na_rep = '*', encoding = 'utf8')