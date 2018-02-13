import csv
import sqlite3

connection = sqlite3.connect("../data/dataBase.db")
cursor = connection.cursor()

# def csv2sql(file) :
with open('../data/equipements_activites.csv', 'r') as f:
    reader = csv.reader(f)
    columns = next(reader)

    try:
        cursor.execute('drop table equipements_activites')
    except sqlite3.OperationalError:
        print('Table non-existant: skipping drop')

    cursor.execute('create table equipements_activites')
    query = 'insert into equipements_activites({0}) values ({1})'
    query = query.format(','.join(columns), ','.join('?' * len(columns)))
    cursor = connection.cursor()
    for data in reader:
        print(query)
        cursor.execute(query, data)
    cursor.commit()