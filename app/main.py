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
<svg width="455" height="1000" xmlns="http://www.w3.org/2000/svg">>
<rect width="500" height="1000" style="fill:white;stroke-width:3;stroke:rgb(0,0,0)" />
<!-- Kasse, Eingang-->
<rect x="0" y="900" width="200" height="150" style="fill:black;stroke:black;stroke-width:5;fill-opacity:0.3;stroke-opacity:1" />
<rect x="250" y="800" width="2500" height="100" style="fill:black;stroke:black;stroke-width:5;fill-opacity:0.3;stroke-opacity:1" />
<text x="25" y="960" fill="#003278" font-size="2.5em">Eingang</text>
<text x="280" y="865" fill="#003278" font-size="3em">Kasse</text>

<!-- Ganz Links -->
<rect x="0" y="450" width="25" height="400" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="0" y="75" width="25" height="325" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- ganz Oben -->
<rect x="0" y="0" width="450" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben 4 -->
<rect x="425" y="75" width="25" height="325" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben 3 -->
<rect x="300" y="75" width="25" height="150" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="325" y="75" width="25" height="150" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="300" width="25" height="75" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="325" y="300" width="25" height="75" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="275" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="375" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben  2-->
<rect x="200" y="75" width="50" height="175" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="200" y="300" width="50" height="100" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Oben 1 -->
<rect x="100" y="75" width="25" height="125" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="125" y="75" width="25" height="125" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="250" width="50" height="125" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="375" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 4 -->
<rect x="425" y="450" width="25" height="300" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 3 -->
<rect x="300" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="325" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="450" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="300" y="725" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 2 -->
<rect x="100" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="125" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="450" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="725" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 1 -->
<rect x="200" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="225" y="475" width="25" height="250" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="200" y="450" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="200" y="725" width="50" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />

<!-- Unten 4 -->
<rect x="100" y="800" width="100" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
<rect x="100" y="825" width="100" height="25" style="fill:#003278;stroke:black;stroke-width:5;fill-opacity:0.5;stroke-opacity:1" />
    
<!-- Location -->
<polygon points="60,850 20,780 100,780" style="fill:#ffe300;stroke:#003278;stroke-width:5" />
<circle cx="60" cy="850" r="20" stroke="#003278" stroke-width="5" fill="#ffe300" id="location" />    
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
    return render_template('navigation.html', time=date_time_str)


@app.route('/map/<user>/map.svg')
def serve_map(user):
    '''
    Das hier sendet den statischen content wie js bilder, mp4 und so....
    '''
    svg = build_map()
    return Response(svg, mimetype='image/svg+xml')


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
