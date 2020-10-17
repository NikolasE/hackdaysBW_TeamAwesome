#!/usr/bin/env python3

import json
from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit, send
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

from map import build_map
from product_locations import product_locations
from pathplanning.pathplanning import Pathplanner

# CONFIG SECTION #
STATIC_URL_PATH = '/static'
SECRET_KEY = 'SOME_SECRET_KEY!'

# Init the server
app = Flask(__name__, static_url_path=STATIC_URL_PATH)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app, logger=False)

coin_list = [(100, 200), (200, 300)]
location = (60,850)
item_list = [(200,700),(200,500)]
path_list = [(100,800),(100,200)]

### helper functions ###

def build_map():
    svg_map = ""

    # Path
    path_str = """<path d="M {0} {1}""".format(location[0], location[1])
    for path in path_list:
        path_str = path_str + "L {} {}".format(path[0], path[1])

    path_str = path_str + """" stroke="black" fill="transparent" style="stroke:gray;stroke-width:10"/>"""

    svg_map = svg_map + path_str

    #Coins
    for coin in coin_list:
        svg_map = svg_map + """
            <ellipse cx="{0}" cy="{1}" rx="20" ry="25" style="fill:#efc501;stroke:#98720b;stroke-width:5" />
	        <line x1="{0}" y1="{2}" x2="{0}" y2="{3}" style="stroke:#98720b;opacity:1;stroke-width:10" />
	        """.format(coin[0], coin[1], coin[1] - 10, coin[1] + 10)

    #Loactaion
    svg_map = svg_map + """
    <!-- Location -->
    <polygon points="{0},{1} {2},{3} {4},{5}" id="location" style="fill:#ffe300;stroke:#003278;stroke-width:5" />
    <circle cx="{0}" cy="{1}" r="20" stroke="#003278" stroke-width="5" fill="#ffe300"/>
    """.format(location[0],location[1], location[0]-40, location[1]-100, location[0]+40, location[1]-100)

    # Items
    for item in item_list:
        svg_map = svg_map + """
        <circle cx="{0}" cy="{1}" r="20" stroke="#003278" stroke-width="5" fill="#ffe300" />
	    <text x="{2}" y="{3}" fill="#003278" font-size="2em">1</text>
	    """.format(item[0],item[1],item[0]-9, item[1]+10)

    svg_end = """</svg>"""
    svg = svg_map + svg_end
    return svg


user_id = 0


@dataclass
class UserData:
    einkaufszettel: list


user_datas = {
    # format: USER_ID: UserData
    # currently there is only user 0
    0: UserData([]),
}


### STATIC FLASK PART ###
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

    user_datas[user_id].einkaufszettel = [item['id'] for item in pizzas]
    print(f'user data is now {user_datas}')

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('einkaufsliste.html', time=date_time_str, pizzas=pizzas)


def _get_path_for_einkaufszettel():
    print(f"We're supposed to collect all these item IDs: {user_datas[user_id].einkaufszettel}")
    # build product locations of only
    locs = [product_locations[id] for id in user_datas[user_id].einkaufszettel]
    print(f"Item locations are: {locs}")
    pp = Pathplanner(map_image_path='pathplanning/map.png', product_locations=locs)
    path = pp.get_path()  # [(0, 0), (0, 1), (0, 1), (0, 2), (0, 3), (0, 4), ...]
    print(f"calculated path is {path}")
    return path

# Das ist die Hauptfunktion die die Seite an sich zurückgibt
@app.route('/navigation')
def navigation():
    path = _get_path_for_einkaufszettel()

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
    # return Response(svg, mimetype='image/svg+xml')
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
