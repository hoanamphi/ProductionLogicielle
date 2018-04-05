import csv
import requests
import sqlite3
import os.path

tables = {['communes'], ['activites_generales'], ['niveau'], ['installations'], ['equipements'], ['activites'])
#Clés étrangère de installations vers communes, de equipements vers installations, de activites vers equipements, de activites vers activites_generales, de activites vers niveau, de activites vers communes

# def makeTables():
#     cursor = connection.cursor()
#     try:
#         cursor.execute('drop table ' + tableName)
#     except sqlite3.OperationalError:
#         print('Table ' + tableName + ' non-existant: skipping drop')

def dictionaryToSQL(array, table, connection):
    cursor = connection.cursor()

def dbcreator(dbPath):
    connection = sqlite3.connect(dbPath)

    installations = requests.get('http://data.paysdelaloire.fr/api/publication/23440003400026_J335/installations_table/content/?format=json').json()
    equipements = requests.get('http://data.paysdelaloire.fr/api/publication/23440003400026_J336/equipements_table/content/?format=json').json()
    activites = requests.get('http://data.paysdelaloire.fr/api/publication/23440003400026_J334/equipements_activites_table/content/?format=json').json()

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
            cursor.execute("SELECT DISTINCT %s FROM %s" % (','.join(attribute), tableName))
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

# effectuer la selectionde critères
def selectCriteria(criteria):
    database = "../data/dataBase.db"
    return select([criteria], "EQUIPEMENTS_ACTIVITES", database)

idCriteriaTable = {0:"ComLib", 1:"ActLib", 2:"ActNivLib"}

def getCriteriaList(id):
    if(id in idCriteriaTable.keys()):
        return sorted(transformFromTupleToArray(selectCriteria(idCriteriaTable[id])))
    else:
        return "INVALID ID"

def transformFromTupleToArray(tuple):
    if(isinstance(tuple, str)):
        return [tuple]
    else:
        return list(sum(tuple, ()))