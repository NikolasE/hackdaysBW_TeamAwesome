#!/usr/bin/env python3
import json
from flask import Flask, render_template, request, Response, redirect
from flask_socketio import SocketIO, emit, send
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from google.cloud import vision
import binascii
import re

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

kasse_location = (999, 400)
pathplanning_locations = list(product_locations.values()) + [kasse_location]
pathplanner = Pathplanner(map_image_path='pathplanning/map.png', locations=pathplanning_locations)


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
        {'id': "0116393",'price': '1.44', 'text': 'Wagner Steinofen', 'url': '/static/wagner.jpeg'},
        {'id': '0007873', 'price': '1.93', 'text': 'kinder bueno', 'url': '/static/kinder_bueno.jpeg'},
        {'id': '0000305', 'price': '1.92', 'text': 'kinder Country', 'url': '/static/kinder_country.jpeg'},
        {'id': '0119704', 'price': '1.32', 'text': 'Bellona', 'url': '/static/bellona.jpeg'},
        {'id': '0001847', 'price': '2.22', 'text': 'kinder Überraschung', 'url': '/static/kinder_suprise.jpeg'},        
        {'id': '0003376', 'price': '1.73', 'text': 'Balisto', 'url': '/static/balisto.jpeg'},
        {'id': '0136673', 'price': '3.21', 'text': 'Koelln Muesli', 'url': '/static/koelln.jpeg'},
        {'id': '0003430', 'price': '0.58', 'text': 'Jodsalz', 'url': '/static/jodsalz.jpeg'},
        {'id': '0047627', 'price': '1.56', 'text': 'Pickup', 'url': '/static/pickup.jpeg'}, 
        {'id': '0001375', 'price': '1.95', 'text': 'Pizza Linsencurry', 'url': '/static/pizza2.jpg'},
        {'id': '0034957', 'price': '1.87', 'text': 'Calabrese Style', 'url': '/static/pizza3.jpg'},
        {'id': '0057475', 'price': '2.57', 'text': 'La Mia Grande', 'url': '/static/pizza4.jpg'},
        {'id': '0098066', 'price': '2.12', 'text': 'Pizza Vegetale', 'url': '/static/pizza5.jpg'},   
        {'id': '0122344', 'price': '1.98', 'text': 'Papa tonis', 'url': '/static/pizza1.jpg'},
        {'id': '0410170', 'price': '0.79', 'text': 'Hefe', 'url': '/static/hefe.jpg'},
        {'id': '0212833', 'price': '7.43', 'text': 'Formil activ', 'url': '/static/formil.png'},
        {'id': '0826492', 'price': '2.46', 'text': 'Fleischwurst', 'url': '/static/fleischwurst.png'},
        {'id': '0926460', 'price': '1.23', 'text': 'Vollmilch', 'url': '/static/milch.png'},
        {'id': '0173628', 'price': '2.50', 'text': 'Tomaten', 'url': '/static/tomaten.jpg'}
    ]

    for counter, item in enumerate(pizzas):
        if item['id'] in user_datas[user_id].einkaufszettel:
            pizzas[counter]["class"] = 'bg-warning'
            pizzas[counter]["inbasket"] = 'true'
        else:
            pizzas[counter]["class"] = 'swatch-400'
            pizzas[counter]["inbasket"] = 'false'

    print(pizzas)

    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('einkaufsliste.html', time=date_time_str, pizzas=pizzas)


def _get_path_for_einkaufszettel(user_location, kasse_location):
    print(f"We're supposed to collect all these item IDs: {user_datas[user_id].einkaufszettel}")
    # build product locations of only
    product_ids = [list(product_locations.keys()).index(id) for id in user_datas[user_id].einkaufszettel]  # TODO plus kasse
    end_id = len(product_ids)-1  # kasse location
    path, route_indices = pathplanner.get_path(user_location, product_ids, end_id)  # [(0, 0), (0, 1), (0, 1), (0, 2), (0, 3), (0, 4), ...], [0 3 2 1]
    print(route_indices)
    route_indices = route_indices[1:-1]
    # route = [product_ids[id-1] for id in route_indices]  # indices to product ids
    route = [list(product_locations.keys())[id-1] for id in route_indices]

    print(f"calculated path is {path} and route is {route}")
    return path, route


@app.route('/navigation')
def navigation():

    user_location = request.args.get('user_location')
    if user_location is not None:
        user_location = eval(user_location)
    else:
        user_location = (850, 60)  # y,x


    coin_list = [(100, 200), (200, 300)]

    kasse_location = (999, 400)

    path_list, item_list = _get_path_for_einkaufszettel(user_location, kasse_location)
    item_locations = [product_locations[id] for id in item_list]

    svg = build_map(coin_list, user_location, item_locations, path_list)
    return render_template('navigation.html', svg=svg, user_x = user_location[0], user_y= user_location[1])


@app.route('/startseite')
def startseite():
    return render_template('startseite.html')


client = vision.ImageAnnotatorClient()


def get_left_right_direction(detected_tags, goal_tag):
    known_tags = ["0003376", "0000305", "0007873", "0119704", "0001847"]
    try:
        goal_ndx = detected_tags.index(goal_tag)
    except ValueError:
        print("Goal tag '%s' is unkown" % goal_tag)
        return None    

    # loop over all tags in case one is invalid
    for t in detected_tags:
        try:
            current_ndx = known_tags.index(t)
            return goal_ndx - current_ndx
        except ValueError:
            continue

    return None
        


import re

@app.route('/whereami', methods=['POST', 'GET'])
def whereami():
    if request.method == 'GET':
        return render_template('video.html')
    else:
        base64 = request.form.get('base64')[22:]
        response = client.annotate_image(
            {'image': {'content': binascii.a2b_base64(base64)} }
        )
        texts = response.text_annotations
        print(texts)
        list_id_numbers = []
        list_boundaries = []
        for text in texts:
            print(text)
            x = re.search(r"(\d{7})\D",str(text))
            if x != None:
                list_boundaries
                list_id_numbers.append(re.sub('\D', '', x.group()))

        if list_id_numbers == 0:
            return render_template('video.html')

        user_location = product_locations[list_id_numbers[0]]

        return redirect("/navigation?user_location={}".format(user_location), code=302)


@app.route('/whereis', methods=['POST', 'GET'])
def whereis():
    if request.method == 'GET':
        hidden = "none"
        text = ""
        return render_template('whereis.html', hidden=hidden, text=text, arrow=0)
    else:
        base64 = request.form.get('base64')[22:]
        response = client.annotate_image(
            {'image': {'content': binascii.a2b_base64(base64)}}  # , 'features': [{'type': "TEXT_DETECTION"}]}
        )
        texts = response.text_annotations
        list_id_numbers = []
        for text in texts:
            x = re.search(r"(\d{7})\D", str(text))
            if x != None:
                list_id_numbers.append(re.sub('\D', '', x.group()))

        print(list_id_numbers)

        if len(list_id_numbers) == 0:
            hidden = "none"
            text = "No tag detected"
        else:
            hidden = "block"
            text = ""

        # Wenn Product in Liste => back

        return render_template('whereis.html', hidden=hidden, text=text, arrow=90)


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

    if data['inbasket'] == 1:
        user_datas[user_id].einkaufszettel.append(data['product'])
    else:
        if data['product'] in user_datas[user_id].einkaufszettel:
            user_datas[user_id].einkaufszettel.remove(data['product'])

    #emit('server_client_namespace', data)
    print(f"einkaufszettel ist: {user_datas[user_id].einkaufszettel}")


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
