import csv
import sqlite3
import Utils

db = '../data/database.db'


Utils.csv2sql('../data/installations.csv', db, 'INSTALLATIONS', ',')
Utils.csv2sql('../data/equipements.csv', db, 'EQUIPEMENTS', ';')
Utils.csv2sql('../data/equipements_activites.csv', db, 'EQUIPEMENTS_ACTIVITES', ',')