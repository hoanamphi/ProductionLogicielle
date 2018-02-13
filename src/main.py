import csv
import sqlite3

connection = sqlite3.connect("data/dataBase.db")
#
cursor = connection.cursor()

# cursor.execute("CREATE TABLE EQUIPEMENTS")
# cursor.execute("CREATE TABLE EQUIPEMENTS_ACTIVITES;")
# cursor.execute("CREATE TABLE INSTALLATIONS;")

with open('data/equipements.csv') as csvfile:
    equipDict = csv.DictReader(csvfile, delimiter=";")
    for row in equipDict:
        first_row = row
        break
    head = ",".join(first_row)
    print(head)
    cursor.execute("CREATE TABLE EQUIPEMENTS ("+head+");")



# with open('data/equipements_activites.csv') as csvfile:
#     equip_actDict = csv.DictReader(csvfile, delimiter=",")
#
# with open('data/installations.csv') as csvfile:
#     installDict = csv.DictReader(csvfile, delimiter=",")
