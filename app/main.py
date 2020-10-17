#!/usr/bin/env python3
import json
from flask import Flask, render_template, request, Response, redirect
from flask_socketio import SocketIO, emit, send
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from google.cloud import vision
import binascii

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

### helper functions ###

def build_map(coin_list, location, item_list, path_list):
    svg_map = ""

    # Path
    path_str = """<path d="M {0} {1}""".format(location[1], location[0])
    for path in path_list:
        path_str = path_str + "L {} {}".format(path[1], path[0])

    path_str = path_str + """" stroke="black" fill="transparent" style="stroke:gray;stroke-width:10"/>"""

    svg_map = svg_map + path_str

    #Coins
    for coin in coin_list:
        svg_map = svg_map + """
            <ellipse cx="{0}" cy="{1}" rx="20" ry="25" style="fill:#efc501;stroke:#98720b;stroke-width:5">
                <animate 
                attributeName="rx" 
                values="20; 2; 20" begin="0s" dur="5s" calcMode="linear" keyTimes="0; 0.5; 1" repeatCount="indefinite"/>
            </ellipse>
	        <line x1="{0}" y1="{2}" x2="{0}" y2="{3}" style="stroke:#98720b;opacity:1;stroke-width:10" />
	        """.format(coin[0], coin[1], coin[1] - 10, coin[1] + 10)

    #Loactaion
    svg_map = svg_map + """
    <!-- Location -->
    <polygon points="{0},{1} {2},{3} {4},{5}" id="location" style="fill:#ffe300;fill-opacity:0.5;stroke:#003278;stroke-width:5" />
    <circle cx="{0}" cy="{1}" r="20" stroke="#003278" stroke-width="5" fill="#ffe300"/>
    """.format(location[1],location[0], location[1]-40, location[0]-100, location[1]+40, location[0]-100)

    # Items
    counter = 0
    for item in item_list:
        svg_map = svg_map + """
        <circle cx="{0}" cy="{1}" r="20" stroke="#003278" stroke-width="5" fill="#ffe300" />
	    <text x="{2}" y="{3}" fill="#003278" font-size="2em">{4}</text>
	    """.format(item[1],item[0],item[1]-9, item[0]+10, counter)
        counter = counter + 1

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
        {'id': "1", 'text': 'Papa Tonis', 'url': '/static/pizza1.jpg'},
        {'id': "2", 'text': 'Pizza Linsencurry', 'url': '/static/pizza2.jpg'},
        {'id': "3", 'text': 'Calabrese Style', 'url': '/static/pizza3.jpg'},
        {'id': "4", 'text': 'La Mia Grande', 'url': '/static/pizza4.jpg'},
        {'id': "5", 'text': 'Pizza Vegetale', 'url': '/static/pizza5.jpg'},
        {'id': "0003376", 'text': 'Balisto', 'url': '/static/pizza5.jpg'},
        {'id': "0007873", 'text': 'kinder bueno', 'url': '/static/pizza5.jpg'},
    ]

    user_datas[user_id].einkaufszettel = [item['id'] for item in pizzas]
    print(f'user data is now {user_datas}')

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('einkaufsliste.html', time=date_time_str, pizzas=pizzas)


def _get_path_for_einkaufszettel(user_location, kasse_location):
    print(f"We're supposed to collect all these item IDs: {user_datas[user_id].einkaufszettel}")
    # build product locations of only
    product_ids = [id for id in user_datas[user_id].einkaufszettel]
    locs = [product_locations[id] for id in product_ids]
    locs = [user_location] + locs + [kasse_location]
    print(f"Item locations are: {locs}")
    pp = Pathplanner(map_image_path='pathplanning/map.png', locations=locs)
    path, route_indices = pp.get_path()  # [(0, 0), (0, 1), (0, 1), (0, 2), (0, 3), (0, 4), ...], [0 3 2 1]

    route = [product_ids[id-1] for id in route_indices]  # indices to product ids

    print(f"calculated path is {path} and route is {route}")
    return path, route


@app.route('/navigation')
def navigation():
    coin_list = [(100, 200), (200, 300)]
    user_location = (850, 60)  # y,x
    kasse_location = (999, 400)

    path_list, item_list = _get_path_for_einkaufszettel(user_location, kasse_location)
    item_locations = [product_locations[id] for id in item_list]

    svg = build_map(coin_list, user_location, item_locations, path_list)
    return render_template('navigation.html', svg=svg, user_x = user_location[0], user_y= user_location[1])


@app.route('/video')
def video():
    return render_template('video.html')


# Temp
client = vision.ImageAnnotatorClient()

@app.route('/whereami', methods=['POST'])
def whereami():

    base64 = request.form.get('base64')[22:]
    print(base64)

    response = client.annotate_image(
        {'image': {'content': binascii.a2b_base64(base64)}})  # , 'features': [{'type': "LABEL_DETECTION"}]})

    #response = client.annotate_image(
    #    {'image': {'content': base64.encode()}})  # , 'features': [{'type': "LABEL_DETECTION"}]})

    print(response)

    return redirect("/video", code=302)


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
