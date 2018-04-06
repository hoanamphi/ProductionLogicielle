# pylint: disable=no-member

from bottle import get, post, run, static_file, request, template, route, response
from Utils import *
from json import *
import numpy as np

# CSS routes
@route('/assets/css/<file>')
def css(file):
    return static_file(file, 'html/assets/css/')

# Image routes
@route('/assets/img/<file>')
def img(file):
    return static_file(file, 'html/assets/img/')

# JS routes
@route('/assets/js/<file>')
def js(file):
    return static_file(file, 'html/assets/js/')

@get('/recherche')
def search_page():
    return static_file('recherche.html', 'html/')

@get('/connexion')
def connexion():
    return static_file('connexion.html', 'html/')

# Recuperer les listes de critères
@post('/api/list')
def search():
    id = request.forms.get('id')
    data = getCriteriaList(int(id))
    json = dumps(data, ensure_ascii=False)
    response.content_type = 'application/json'
    return json

# Recuperer les listes de critères
@post('/api/login')
def login():
    id = request.forms.get('id')
    mdp = request.forms.get('mdp')
    if (id == "admin" and mdp == "1234"):
        json = dumps("true", ensure_ascii=False)
        # dbCreator('data/database.db')
    else:
        json = dumps("false", ensure_ascii=False)
    response.content_type = 'application/json'
    return json

@post('/api/search')
def results():
    discipline = request.forms.get('discipline')
    commune = request.forms.get('commune')
    niveau = request.forms.get('niveau')
    desserte = request.forms.get('desserte')
    nominstall = request.forms.get('nom_installation')

    install1 = selectNumeroIns(discipline, commune, niveau)
    install2 = selectInstallation(nominstall)
    if(len(install1) == 0):
        if(len(install2) == 0):
            data = []
        else:
            data = selectInstallationInfos(install2, desserte)
    else:
        if(len(install2) == 0):
            data = selectInstallationInfos(install1, desserte)
        else:
            data = selectInstallationInfos(np.intersect1d(install1, install2), desserte)

    json = dumps(data, ensure_ascii=False)
    response.content_type = 'application/json'
    return json

run(host='localhost', port=8080, debug=True)
