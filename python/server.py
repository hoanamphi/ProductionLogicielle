# pylint: disable=no-member

from bottle import get, post, run, static_file, request, template, route, response
from python.Utils import *
from json import *

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

@post('/api/list')
def search():
    id = request.forms.get('id')
    data = getCriteriaList(int(id))
    json = dumps(data)
    response.content_type = 'application/json'
    # return template('result.tpl', list=json)
    return json #je sais pas si ça marche comme ça

run(host='localhost', port=8080, debug=True)
