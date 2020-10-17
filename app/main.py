#!/usr/bin/env python3

import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit, send
from datetime import datetime
from pathlib import Path

from map import build_map
from product_locations import product_locations

# CONFIG SECTION #
STATIC_URL_PATH = '/static'
SECRET_KEY = 'SOME_SECRET_KEY!'

# Init the server
app = Flask(__name__,  static_url_path=STATIC_URL_PATH)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, logger=False)



### STATIC FLASK PART ###

# Das ist die Hauptfunktion die die Seite an sich zurückgibt
@app.route('/')
def main():
    '''
    Main flask function returning the website
    Serving a website from a function only makes sense if you actually add some dynamic content to it...
    We will send the current time.
    '''

    # IDs correspond to the ones in `product_locations`
    pizzas = [
        {'id': 1, 'text': 'Papa Tonis', 'url': '/static/pizza1.jpg'},
        {'id': 2, 'text': 'Pizza Linsencurry', 'url': '/static/pizza2.jpg'},
        {'id': 3, 'text': 'Calabrese Style', 'url': '/static/pizza3.jpg'},
        {'id': 4, 'text': 'La Mia Grande', 'url': '/static/pizza4.jpg'},
        {'id': 5, 'text': 'Pizza Vegetale', 'url': '/static/pizza5.jpg'},
    ]

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('einkaufsliste.html', time=date_time_str, pizzas=pizzas)


# Das ist die Hauptfunktion die die Seite an sich zurückgibt
@app.route('/navigation')
def navigation():

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('navigation.html', time=date_time_str)

@app.route('/map/')
def map():
    svg = build_map()
    return render_template('index.html', svg=svg)

@app.route('/map/<user>/map.svg')
def serve_map(user):
    '''
    Das hier sendet den statischen content wie js bilder, mp4 und so....
    '''
    svg = build_map()
    #return Response(svg, mimetype='image/svg+xml')
    return Response(svg)


@app.route('/static/<path:path>')
def serve_static(path):
    '''
    Das hier sendet den statischen content wie js bilder, mp4 und so....
    '''
    return send_from_directory('static', path)


### SOCKET FLASK PART ###
# Receive a message from the front end HTML
@socketio.on('client_server_namespace')
def message_recieved(data):
    '''
    This receaves dynamic content which can then be used for anything else...
    We are just going to send it back to the client to adjust the value displyed 
    Using emit will send the Data to all client which are connencted...
    '''
    print(data)
    emit('server_client_namespace', data)


def _get_ssl_context():
    fullchain = Path('/etc/letsencrypt/live/woistdiehefe.latai.de/fullchain.pem')
    privkey = Path('/etc/letsencrypt/live/woistdiehefe.latai.de/privkey.pem')
    if fullchain.is_file() and privkey.is_file():
        ssl_context = (fullchain, privkey)
    else:
        ssl_context = 'adhoc'
    return ssl_context


# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """

    socketio.run(app, ssl_context=_get_ssl_context(), host="0.0.0.0", port=8000, debug=True)
