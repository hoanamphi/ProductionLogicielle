import csv
import sqlite3

connection = sqlite3.connect("data/dataBase.db")
cursor = connection.cursor()

def csv2sql(file) :
    with open(file, 'r') as f:
        reader = csv.reader(f)
        columns = next(reader)

        query = 'insert into MyTable({0}) values ({1})'
        query = query.format(','.join(columns), ','.join('?' * len(columns)))
        cursor = connection.cursor()
        for data in reader:
            cursor.execute(query, data)
        cursor.commit()