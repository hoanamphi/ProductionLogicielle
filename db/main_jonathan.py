import csv
import sqlite3
import Utils

# db = '../data/database.db'
#
#
# res = Utils.select('ComInsee',db, 'EQUIPEMENTS')
# if(isinstance(res, str)):
#     print(res)
# else:
#     for row in res:
#         print(row)

db = '../data/database.db'


res = Utils.selectWhere("EquipementTypeLib",{"ComInsee":44001,"InsNom":"Site De La Mine"},db, 'EQUIPEMENTS')
if(isinstance(res, str)):
    print(res)
else:
    for row in res:
        print(row)