from flask import Flask, render_template, Response, request, redirect
from werkzeug.utils import secure_filename
import sys
import os
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
    

# Upload mp3 file
app.config['UPLOAD_FOLDER'] = 'music/uploads'
app.config['MAX_CONTENT_PATH'] = 1000000000 # bytes (arbitrary for now)
ALLOWED_EXTENSIONS = {'mp3','mp4'} # add to this

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/') #unsure what the url would be? test
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
    return "success!"


#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    
