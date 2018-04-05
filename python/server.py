# pylint: disable=no-member

from bottle import get, post, run, static_file, request, template, route

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

run(host='localhost', port=8080, debug=True)
