import pandas as pd 


print('Считывание данных....')
#Считывание данных из csv файла
data = pd.read_csv('brooklyn_sales_map.csv', sep = ',')

print('запись данных....')
#Поиск уникальных значений в столбце building_class_category
SearchBuildingClassCategory = data['building_class_category'].unique()
for ColumnsName in SearchBuildingClassCategory:
    SearchResult = data.loc[data['building_class_category'] == ColumnsName]
    SearchResult.to_csv(str(ColumnsName).replace("/"," ") + '.csv')

print('Подсчет значений....')  
#Выборка столбцов, в которых есть числа
ColumnsName = data.select_dtypes(include='number').columns
for Columns in ColumnsName:
    print('Столбец - ' + Columns)
    print('Количество пропущенных значений = ' + str(data[Columns].isna().sum()))
    print('Cреднее значение = ' + str(data[Columns].mean()))
    print('Медиана = ' + str(data[Columns].median()))
    print('Наибольшее значение = ' + str(data[Columns].max()))
    print('Наименьшее значение = ' + str(data[Columns].min()))
    print('Количество уникальных значений = ' + str(len(data[Columns].unique())))
    print('******************')
    
print('\n')
for Columns in SearchBuildingClassCategory:
    try:
        part=data['building_class_category'].value_counts()[Columns]/len(data['building_class_category'].values)
        print(Columns + ': доля значения поля (building_class_category) = ' + str(part))
    except:
        continue
    
print('Нормализация данных....')    
data2 = (data._get_numeric_data() - data._get_numeric_data().min())/(data._get_numeric_data().max() - data._get_numeric_data().min())
data2.to_csv('Нормализация.csv')
    