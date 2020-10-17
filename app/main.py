#!/usr/bin/env python3

import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit, send
from datetime import datetime
from pathlib import Path

# CONFIG SECTION #
STATIC_URL_PATH = '/static'
SECRET_KEY = 'SOME_SECRET_KEY!'

# Init the server
app = Flask(__name__,  static_url_path=STATIC_URL_PATH)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, logger=False)

### helper functions ###


def build_map():
    svg_map = """
    <!-- Location -->
    <polygon points="60,850 20,780 100,780" id="location" style="fill:#ffe300;stroke:#003278;stroke-width:5" />
    <circle cx="60" cy="850" r="20" stroke="#003278" stroke-width="5" fill="#ffe300"/>    
    """

    svg_end = """</svg>"""
    svg = svg_map + svg_end

    return svg

### STATIC FLASK PART ###

# Das ist die Hauptfunktion die die Seite an sich zurückgibt
@app.route('/')
def main():
    '''
    Main flask function returning the website
    Serving a website from a function only makes sense if you actually add some dynamic content to it...
    We will send the current time.
    '''
    pizzas = [
        {'name': 'pizza1', 'text': 'Papa Tonis', 'url': '/static/pizza1.jpg'},
        {'name': 'pizza2', 'text': 'Pizza Linsencurry', 'url': '/static/pizza2.jpg'},
        {'name': 'pizza3', 'text': 'Calabrese Style', 'url': '/static/pizza3.jpg'},
        {'name': 'pizza4', 'text': 'La Mia Grande', 'url': '/static/pizza4.jpg'},
        {'name': 'pizza5', 'text': 'Pizza Vegetale', 'url': '/static/pizza5.jpg'},
    ]

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('einkaufsliste.html', time=date_time_str, pizzas=pizzas)

# Das ist die Hauptfunktion die die Seite an sich zurückgibt
@app.route('/navigation')
def navigation():

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    svg = build_map()
    return render_template('navigation.html', svg=svg, time=date_time_str)


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
