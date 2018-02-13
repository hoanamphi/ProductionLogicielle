import csv
import sqlite3


def csv2sql(csvFile, dbFile, tableName, d):
    connection = sqlite3.connect(dbFile)
    cursor = connection.cursor()

    with open(csvFile, 'r') as f:
        reader = csv.DictReader(f, delimiter=d)
        columns = next(reader)

        try:
            cursor.execute('drop table ' + tableName)
        except sqlite3.OperationalError:
            print('Table ' + tableName + ' non-existant: skipping drop')

        columns = list(columns)
        columns = map(lambda s : "`"+s+"`", columns)
        columns = list(columns)

        cursor.execute('create table ' + tableName + ' (' + ','.join(columns) + ')')
        query = 'insert into ' + tableName + '({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))

        for data in reader:
            print(query)
            cursor.execute(query, list(data.values()))
        connection.commit()


def printCsv(csvFile, d):
    with open(csvFile, 'r') as f:
        reader = csv.DictReader(f, delimiter=d)
        for row in reader:
            print(row)
