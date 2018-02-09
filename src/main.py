import csv


def init():
    with open('data/equipements.csv') as csvfile:
        equipDict = csv.DictReader(csvfile, delimiter=";")
    with open('data/equipements_activites.csv') as csvfile:
        equip_actDict = csv.DictReader(csvfile, delimiter=",")
    with open('data/installations.csv') as csvfile:
        installDict = csv.DictReader(csvfile, delimiter=",")
'''def search(ComInsee, ComLib):
    init()
    result = [];
    for row in equipDict:
        if(row['ComInsee'] == ComInsee and row['ComLib'] == ComLib):
            result.append(row);
    return result'''