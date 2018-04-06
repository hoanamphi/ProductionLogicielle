import requests
import sqlite3
import os.path

class DbCreatorException(Exception):
    pass


def dataToSQL(columns, datalist, table, cursor):
	query = 'insert into %s ({0}) values ({1})' % (table)
	query = query.format(','.join(columns), ','.join('?' * len(columns)))
	for data in datalist:	
		cursor.execute(query, list(data.values()))
	
def makeIndex(values):
	for i, value in enumerate(values):
		value['manualIndex'] = i
	
def makeTables(connection, tablesToProcess):
	cursor = connection.cursor()
	tables = {}
	order = []
	while(len(tablesToProcess) > 0):
		processed = 0
		for name, table in { k : v for k,v in tablesToProcess.items() }.items():
			valid = True;
			foreign_keys = ''
			for fk in table['foreign_keys']:
				if not fk['dst'] in tables.keys():
					valid = False
					break
				foreign_keys += ", CONSTRAINT %s%s FOREIGN KEY (%s) REFERENCES %s (%s)" % (name, fk['dst'], fk['src'], fk['dst'], tables[fk['dst']]['primary_key'])
			if not valid:
				continue
			if(table['primary_key'] == "manualIndex"):
				makeIndex(table['values'])
			columns = table['values'][0].keys()
			columns = ','.join(columns)
			table['creator'] = "CREATE TABLE %s (%s, PRIMARY KEY (%s)%s)" % (name, columns, table['primary_key'], foreign_keys)
			tables[name] = table
			del tablesToProcess[name]
			order.append(name)
			processed += 1
		if processed == 0:
			raise DbCreatorException("Incorrect constraints!")
	for name in order:
		try:
			cursor.execute('DROP TABLE %s' % (name))
		except sqlite3.OperationalError:
			print('Table %s non-existant: skipping drop' % (name))
		cursor.execute(tables[name]['creator'])
		columns = list(tables[name]['values'][0].keys())
		data = list(tables[name]['values'])
		dataToSQL(columns, data, name, cursor)
	
def getCommunes(installations, equipements, activites):
	communes = {}
	for installation in installations:
		communes[installation['ComInsee']] = {'ComInsee': installation['ComInsee'], 'ComLib': installation['ComLib']}
		del installation['ComLib']
		del installation['_l']
		del installation['geo']
	for equipement in equipements:
		communes[equipement['ComInsee']] = {'ComInsee': equipement['ComInsee'], 'ComLib': equipement['ComLib']}
		del equipement['ComLib']
	for activite in activites:
		communes[activite['ComInsee']] = {'ComInsee': activite['ComInsee'], 'ComLib': activite['ComLib']}
		del activite['ComLib']
	return list(communes.values())
	
def getDisciplines(activites):
	disciplines = {}
	for activite in activites:
		disciplines[activite['ActCode']] = {'ActCode': activite['ActCode'], 'ActLib': activite['ActLib']}
		del activite['ActLib']
	del disciplines[None]
	return list(disciplines.values())
	
def getNiveaux(activites):
	niveaux = {}
	for activite in activites:
		niveaux[activite['ActNivLib']] = {'ActNivId': '0', 'ActNivLib': activite['ActNivLib']}
	for i, niveau in enumerate(niveaux.values()):
		niveau['ActNivId'] = str(i)
	for activite in activites:
		activite['ActNivId'] = niveaux[activite['ActNivLib']]['ActNivId']
		del activite['ActNivLib']
	del niveaux[None]
	del niveaux['Non défini']
	return list(niveaux.values())

def dbCreatorImpl(connection):
	installations = requests.get('http://data.paysdelaloire.fr/api/publication/23440003400026_J335/installations_table/content/?format=json').json()['data']
	equipements = requests.get('http://data.paysdelaloire.fr/api/publication/23440003400026_J336/equipements_table/content/?format=json').json()['data']
	#equipements = [{'EquipementId': '00', 'ComInsee': '44000', 'ComLib': '00', 'InsNumeroInstall': '00000'}]
	activites = requests.get('http://data.paysdelaloire.fr/api/publication/23440003400026_J334/equipements_activites_table/content/?format=json').json()['data']
	
	communes = getCommunes(installations, equipements, activites)
	disciplines = getDisciplines(activites)
	niveaux = getNiveaux(activites)
	
	tables = {'communes':{'primary_key': 'ComInsee', 'foreign_keys':[], 'values':communes},
	'disciplines':{'primary_key': 'ActCode', 'foreign_keys':[], 'values':disciplines},
	'niveaux':{'primary_key': 'ActNivId', 'foreign_keys':[], 'values':niveaux},
	'installations':{'primary_key': 'InsNumeroInstall', 'foreign_keys':[{'src': 'ComInsee', 'dst': 'communes'}], 'values':installations},
	'equipements':{'primary_key': 'EquipementId', 'foreign_keys':[{'src': 'ComInsee', 'dst': 'communes'}, {'src': 'InsNumeroInstall', 'dst': 'installations'}], 'values':equipements},
	'activites':{'primary_key': 'manualIndex', 'foreign_keys':[{'src': 'ComInsee', 'dst': 'communes'}, {'src': 'EquipementId', 'dst': 'equipements'}, {'src': 'ActCode', 'dst': 'disciplines'}, {'src': 'ActNivId', 'dst': 'niveaux'}], 'values':activites}}
	
	makeTables(connection, tables)
	
def dbCreator(dbPath):
	connection = sqlite3.connect(dbPath)
	
	try:
		dbCreatorImpl(connection)
		connection.commit()
	except Exception as e:
		connection.rollback()

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

def selectCriteria(criteria, tableName):
    database = "../data/dataBase.db"
    return select([criteria], tableName, database)

idCriteriaTable = {0:"ComLib", 1:"ActLib", 2:"ActNivLib", 3:"InsNom"}

def getCriteriaList(id):
    if(id in idCriteriaTable.keys()):
        if(id == 0):
            return sorted(transformFromTupleToArray(selectCriteria(idCriteriaTable[id], "communes")))
        if (id == 1):
            return sorted(transformFromTupleToArray(selectCriteria(idCriteriaTable[id], "disciplines")))
        if (id == 2):
            return sorted(transformFromTupleToArray(selectCriteria(idCriteriaTable[id], "niveaux")))
        if (id == 3):
            return sorted(transformFromTupleToArray(selectCriteria(idCriteriaTable[id], "equipements")))
    else:
        return "INVALID ID"

#
def selectWhere1Attribute(selectedAttribute, tableName, conditionAttribute, conditionsValue, dbFile):
    if os.path.isfile(dbFile):
        connection = sqlite3.connect(dbFile)
        cursor = connection.cursor()
        if(len(conditionsValue)>100):
            conditionsValue = conditionsValue[:100]
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
#
def transformFromTupleToArray(tuple):
    if(isinstance(tuple, str)):
        return [tuple]
    else:
        return list(sum(tuple, ()))
#
def selectNumeroIns(activityName, commune, niveau):
    Equipementid = []
    db = "../data/dataBase.db"
    if(activityName != ""):
        code = transformFromTupleToArray(selectWhere1Attribute(["ActCode"], "disciplines", "ActLib", [activityName], db))
        result = selectWhere1Attribute(["EquipementId"], "activites", "ActCode", code, db)
        if(len(Equipementid) != 0):
            Equipementid = np.intersect1d(Equipementid, transformFromTupleToArray(result))
        else:
            Equipementid = transformFromTupleToArray(result)

    if (niveau != ""):
        code = transformFromTupleToArray(
            selectWhere1Attribute(["ActNivId"], "niveaux", "ActNivLib", [niveau], db))
        result = selectWhere1Attribute(["EquipementId"], "activites", "ActNivId", code, db)
        if (len(Equipementid) != 0):
            Equipementid = np.intersect1d(Equipementid,transformFromTupleToArray(result))
        else:
            Equipementid = transformFromTupleToArray(result)

    numeroIns = transformFromTupleToArray(selectWhere1Attribute(["InsNumeroInstall"], "equipements", "EquipementId", Equipementid, db))

    if (commune != ""):
        code = transformFromTupleToArray(
            selectWhere1Attribute(["ComInsee"], "communes", "ComLib", [commune], db))
        result = selectWhere1Attribute(["InsNumeroInstall"], "installations", "ComInsee", code, db)
        if (len(numeroIns) != 0):
            numeroIns = np.intersect1d(numeroIns, transformFromTupleToArray(result))
        else:
            numeroIns = transformFromTupleToArray(result)

    return numeroIns

def selectInstallation(nom_install):
    numeroIns = []
    db = "../data/dataBase.db"

    if (nom_install != ""):
        result = selectWhere1Attribute(["InsNumeroInstall"], "equipements", "InsNom", [nom_install], db)
        if (len(numeroIns) != 0):
            numeroIns = np.intersect1d(numeroIns, transformFromTupleToArray(result))
        else:
            numeroIns = transformFromTupleToArray(result)
    return numeroIns

def selectInstallationInfos(numeroIns, desserte):
    if(len(numeroIns)) == 0:
        return []
    else:
        db = "../data/dataBase.db"
        result = []
        for numero in numeroIns:
            tmp = []
            insNom = transformFromTupleToArray(selectWhere1Attribute(["InsNom"], "equipements", "InsNumeroInstall", [numero], db))
            tmp.insert(0,insNom[0])
            comInsee = transformFromTupleToArray(selectWhere1Attribute(["ComInsee"], "equipements", "InsNumeroInstall", [numero], db))
            comLib = transformFromTupleToArray(selectWhere1Attribute(["ComLib"], "communes", "ComInsee", comInsee, db))
            tmp.insert(1, comLib[0])
            infos = ["InsCodePostal", "InsLieuDit", "InsLibelleVoie", "InsNoVoie", "InsInternat", "InsNbPlaceParking"]
            for item in transformFromTupleToArray(
                    selectWhere1Attribute(infos, "installations", "InsNumeroInstall", [numero], db)):
                tmp.append(item)
            result.append(tmp)
        return result

def checkDesserte(numeroIns , desserte):
    if(desserte != ""):
        db = "../data/dataBase.db"
        table = "installations"
        if(desserte == "bus"):
            test = selectWhere1Attribute(["InsTransportBus"], table, "InsNumeroInstall", numeroIns, db)
        if (desserte == "tram"):
            test = selectWhere1Attribute(["InsTransportTram"], table, "InsNumeroInstall", numeroIns, db)
        if (desserte == "train"):
            test = selectWhere1Attribute(["InsTransportTrain"], table, "InsNumeroInstall", numeroIns, db)
        if (desserte == "autre"):
            test = selectWhere1Attribute(["InsTransportAutre"], table, "InsNumeroInstall", numeroIns, db)
        if (desserte == "metro"):
            test = selectWhere1Attribute(["InsTransportMetro"], table, "InsNumeroInstall", numeroIns, db)
        if (desserte == "bateau"):
            test = selectWhere1Attribute(["InsTransportBateau"], table, "InsNumeroInstall", numeroIns, db)
        return transformFromTupleToArray(test)
    else:
        return "Pas de desserte"