import csv
import sqlite3
import os.path


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

def select(attribute, tableName, dbFile):
    if os.path.isfile(dbFile):
        connection = sqlite3.connect(dbFile)
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT %s FROM %s" % (','.join(attribute), tableName))
            return cursor.fetchall()
        except sqlite3.OperationalError as exception:
            return str(exception)
    else:
        return "no such database : "+dbFile

def selectWhere1Attribute(selectedAttribute, tableName, conditionAttribute, conditionsValue, dbFile):
    if os.path.isfile(dbFile):
        connection = sqlite3.connect(dbFile)
        cursor = connection.cursor()

        attribute = ','.join(selectedAttribute)
        values = ','.join('?' for i in conditionsValue)
        query = "SELECT %s FROM %s WHERE %s IN (%s)" % (attribute, tableName, conditionAttribute, values)
        try:
            cursor.execute(query, conditionsValue,)
            return cursor.fetchall()
        except sqlite3.OperationalError as exception:
            return str(exception)
    else:
        return "no such database : " + dbFile

def selectEquipementFromActivity(activityName, dbFile):
     return selectWhere1Attribute(["EquipementId"], "EQUIPEMENTS_ACTIVITES", "ActLib", activityName, dbFile)


