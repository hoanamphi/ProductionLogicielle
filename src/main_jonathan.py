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


# res = Utils.selectWhere("*",{"EquipementId":129515},db, 'EQUIPEMENTS_ACTIVITES')
# if(isinstance(res, str)):
#     print(res)
# else:
#     for row in res:
#         print(row)

res = Utils.selectEquipementFromActivity(["Football / Football en salle (Futsal)"], db)
if(isinstance(res, str)):
    print(res)
else:
    for row in res:
        print(row)

# res = Utils.selectWhere1Attribute(["EquipementId, ActLib"], "EQUIPEMENTS", "EquipementId", ['129515','197752'], db)
# if(isinstance(res, str)):
#     print(res)
# else:
#     for row in res:
#         print(row)