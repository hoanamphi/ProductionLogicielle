# pylint: disable=no-member

from bottle import get, post, run, static_file, request, template


@get('/recherche')
def search_page():
    return static_file('index.html', 'html/')

@post('/recherche')
def search():
    dictio = {'INomActivite': request.forms.get('INomActivite')}
    return template('html/result', **dictio)

run(host='localhost', port=8080, debug=True)
