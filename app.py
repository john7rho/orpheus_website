from flask import Flask,render_template, Response
import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


def return_dict():
    #Dictionary to store music file information
    dict_here = [
        {'id': 0, 'name': 'Bass', 'link': 'music/ybwm_bass.mp3', 'genre': 'N', 'rating': 4},
        {'id': 1, 'name': 'Drums', 'link': 'music/ybwm_drums.mp3', 'genre': 'Bollywood', 'rating': 4},
        {'id': 2, 'name': 'Vocals', 'link': 'music/ybwm_vocals.mp3', 'genre': 'Bollywood', 'rating': 4},
        {'id': 3, 'name': 'Piano', 'link': 'music/ybwm_piano.mp3', 'genre': 'Bollywood', 'rating': 4},
        {'id': 4, 'name': 'Other', 'link': 'music/ybwm_other.mp3', 'genre': 'Bollywood', 'rating': 4}
        ]
    return dict_here

# Initialize Flask.
app = Flask(__name__)


#Route to render GUI
@app.route('/')
def show_entries():
    general_Data = {
        'title': 'Music Player'}
    return render_template('simple.html')

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    
