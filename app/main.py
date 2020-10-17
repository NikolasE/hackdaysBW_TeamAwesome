import json 
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, send
from datetime import datetime

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
    pizzas = [{'name': 'pizza1','text': 'Papa Tonis', 'url': '/static/pizza1.jpg'},
           {'name': 'pizza2','text': 'Pizza Linsencurry', 'url': '/static/pizza2.jpg'},
           {'name': 'pizza3','text': 'Calabrese Style', 'url': '/static/pizza3.jpg'},
           {'name': 'pizza4','text': 'La Mia Grande', 'url': '/static/pizza4.jpg'},
           {'name': 'pizza5','text': 'Pizza Vegetale', 'url': '/static/pizza5.jpg'}]
    now = datetime.now()
    date_time_str = now.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('einkaufsliste.html', time=date_time_str,pizzas=pizzas)


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


# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """    
    socketio.run(app, port=8000, debug=True)
