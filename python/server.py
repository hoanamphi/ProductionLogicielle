# pylint: disable=no-member

from bottle import get, post, run, static_file, request, template, route
from python.Utils import *

# CSS routes
@route('/assets/css/<file>')
def css(file):
    return static_file(file, 'html/assets/css/')

# Image routes
@route('/assets/img/<file>')
def img(file):
    return static_file(file, 'html/assets/img/')

@get('/recherche')
def search_page():
    return static_file('recherche.html', 'html/')


# Recuperer les listes de critères
@get('/api/list')
def search_page():
    return static_file('list_formulaire.html', '../html/')

@post('/api/list')
def search():
    id = request.forms.get('id')
    data = getCriteriaList(int(id))
    json = dumps(data)
    return template('result.tpl', list=json)

run(host='localhost', port=8080, debug=True)
