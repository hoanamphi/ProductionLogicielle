import csv
import sqlite3
import Utils

db = '../data/database.db'


res = Utils.select('ComInsee',db, 'EQUIPEMENTS')
if(isinstance(res, str)):
    print(res)
else:
    for row in res:
        print(row)