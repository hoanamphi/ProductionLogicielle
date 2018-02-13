import csv
import sqlite3

connection = sqlite3.connect("data/test.db")

cursor = connection.cursor()
cursor.execute("CREATE TABLE EQUIPEMENTS (ComInsee INT, Com)")

with open('data/equipements.csv') as csvfile:
    equipDict = csv.DictReader(csvfile, delimiter=";")


with open('data/equipements_activites.csv') as csvfile:
    equip_actDict = csv.DictReader(csvfile, delimiter=",")

with open('data/installations.csv') as csvfile:
    installDict = csv.DictReader(csvfile, delimiter=",")

