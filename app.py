from flask import Flask, render_template, Response, request, redirect, flash
from werkzeug.utils import secure_filename
import sys
import os
from os import listdir
from os.path import isfile, join
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

# Initialize Flask.
app = Flask(__name__)
app.secret_key = 'secretkey'

# Set folder for uploads
UPLOAD_FOLDER = 'static\\uploads' # TODO path breaks depending on OS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set folder for stems
STEM_FOLDER = 'static\\stems' # TODO path breaks depending on OS - macOS works with single slash
PITCHED_FOLDER = 'static/pitched'

# Get list of all uploaded songs
songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

#Route to render GUI
@app.route('/')
def show_entries():
    general_Data = {
        'title': 'Music Player'}
    return render_template('simple.html', songs=songs)
    

# Upload mp3 file. in the future, save this to sql database
app.config['MAX_CONTENT_PATH'] = 1000000000 # bytes (arbitrary for now)
ALLOWED_EXTENSIONS = {'mp3','mp4'} # add to this

# Allow file if it is a file type in the allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Do not allow more than one period in a file's name
def allowed_name(filename):
    return len(filename.split('.')) == 2

# TODO reject song if already uploaded
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
        if (allowed_name(file.filename) == False):
            flash('File name must not have period outside of file type extension')
            return redirect('/')
        if file and allowed_file(file.filename) and allowed_name(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Update list of songs
            songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))] # need to append
            return render_template("simple.html", songs=songs)
    return "success!"


# Spleeter
@app.route('/spleeter', methods=['GET', 'POST'])
def spleeter():
    if request.method == 'POST':
        
        # TODO: Alert the user that this may take a minute
        
        # TODO: stop the user from spleeting if a stem directory already exists. or at least do something that stops this from trying to make 2 folders with the same name.
        
        # Get song file path
        song = request.form.get('song')
        
        # Correct path to include working directory
        song_path = join(UPLOAD_FOLDER, song)
        
        # Isolate song name
        song_name = song.rsplit('.', 1)[0] # TODO write better code
        
        # New directory for song's stems
        new_folder = join(STEM_FOLDER, song_name)
        
        # Make a directory for the song's stems
        os.system(f"mkdir {new_folder}")
        
        # Spleet the song. TODO: PLEASE CHECK that this works (it should put stems in the stem folder)
        os.system(f"spleeter separate {song_path} -p spleeter:5stems -o {new_folder}")

        # Create list of stems. TODO: if spleeter works double check which file it sends the stems to. (it might send them to an 'output' folder under the new_folder)
        stems = [f for f in listdir(new_folder) if isfile(join(new_folder, f))]
        
        # testing
        test = [song_path]

        # add the songs
        songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

        return render_template("simple.html", songs=songs, stems=stems)

# Pitch shifter
@app.route('/shifter', methods=['GET', 'POST'])
def shifter():
    if request.method == 'POST':
        
        # TODO: Alert the user that this may take a minute
        
        # TODO: stop the user from spleeting if a stem directory already exists. or at least do something that stops this from trying to make 2 folders with the same name.
        
        # Get song file path
        song = request.form.get('song')
        
        # Isolate song name
        song_name = song.rsplit('.', 1)[0] # TODO write better code

        # Correct path to include working directory
        song_path = 'static/stems/' + song_name + '/' + song_name
        
        # New directory for song's stems
        new_folder = 'static/pitched/' + song_name
        new_path = 'static\\pitched\\' + song_name

        # Paths for current stems and pitched stems
        current_vocals = song_path + '/vocals.wav'
        current_bass = song_path + '/bass.wav'
        current_other = song_path + '/other.wav'
        current_piano = song_path + '/piano.wav'
        current_drums = song_path + '/drums.wav'
        
        shift_vocals = new_folder + '/vocals.wav'
        shift_bass = new_folder + '/bass.wav'
        shift_other = new_folder + '/other.wav'
        shift_piano = new_folder + '/piano.wav'
        shift_drums = new_folder + '/drums.wav'

        #TODO only let the pitch work if song is already spleeted
        
        #TODO add a blending feature also to blend in background vocals

        # Make folder for the new pitched stems
        os.system(f"mkdir {new_path}")

        # Spleet the song. TODO: PLEASE CHECK that this works (it should put stems in the stem folder)
        os.system(f"pitchshifter -s {current_vocals} -o {shift_vocals} -p 1 -b 1")
        os.system(f"pitchshifter -s {current_bass} -o {shift_bass} -p 1 -b 1")
        os.system(f"pitchshifter -s {current_other} -o {shift_other} -p 1 -b 1")
        os.system(f"pitchshifter -s {current_piano} -o {shift_piano} -p 1 -b 1")
        os.system(f"pitchshifter -s {current_drums} -o {shift_drums} -p 1 -b 1")

        # Create list of stems. TODO: if spleeter works double check which file it sends the stems to. (it might send them to an 'output' folder under the new_folder)
        pitched_stems = [f for f in listdir(new_folder) if isfile(join(new_folder, f))]
        
        # testing
        test = [song_path]

        return render_template("simple.html", songs=songs, stems=pitched_stems)

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    
