from flask import Flask, render_template, Response, request, redirect, flash, send_from_directory, session
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from cs50 import SQL
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

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///orpheus.db")

# Set folder for uploads
UPLOAD_FOLDER = 'static/uploads' # TODO path breaks depending on OS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set folder for stems
STEM_FOLDER = 'static/stems' # TODO path breaks depending on OS - macOS works with single slash
PITCHED_FOLDER = 'static/pitched'

# Configure upload information
app.config['MAX_CONTENT_PATH'] = 1000000000 # bytes (arbitrary for now)
ALLOWED_EXTENSIONS = {'mp3','mp4'} # add to this

# Get list of all uploaded songs
#songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

# TODO: if time, put in helpers.py for design
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Orpheus home page
@app.route('/')
def show_entries():
    return render_template('index.html')

# Display the songs that the user has uploaded
@app.route('/mysongs')
@login_required
def show_songs():

    # when we do dbexecute, check to make sure len != 0. if ln = 0 flash you have not ...
    # get all songs using db.execute
    # order them alphabetically
    pathless_songs = db.execute("SELECT song FROM songs WHERE user_id=?", session["user_id"])

    if len(pathless_songs) == 0:
        flash("You have not uploaded any songs yet.")
        return redirect('/upload')

    return render_template("mysongs.html", songs=pathless_songs)


# Allow file if it is a file type in the allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Do not allow more than one period in a file's name
def allowed_name(filename):
    return len(filename.split('.')) == 2

# TODO reject song if already uploaded
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part.')
            return redirect('/') #unsure what the url would be? test
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file.')
            return redirect('/')
        if (allowed_name(file.filename) == False):
            flash('File name must not contain a period.')
            return redirect('/')
        if file and allowed_file(file.filename) and allowed_name(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Insert song into database
            db.execute("INSERT INTO songs (song, user_id) VALUES(?,?)", filename, session["user_id"])

            # Update list of songs
            songs = db.execute("SELECT song FROM songs WHERE user_id=?", session["user_id"])

            return render_template("mysongs.html", songs=songs)

    return render_template("upload.html")


# Spleeter
@app.route('/spleeter', methods=['GET', 'POST'])
@login_required
def spleeter():
    if request.method == 'POST':
        
        # TODO: Alert the user that this may take a minute
                
        # Get song file path
        song = request.form.get('song')
        
        # Correct path to include working directory
        song_path = join(UPLOAD_FOLDER, song)
        
        # Isolate song name
        song_name = song.rsplit('.', 1)[0]

        # If folder exists, stems already exist
        if song_name in [song for song in listdir(STEM_FOLDER)]:

            # Generate a list of stem paths
            stems = [STEM_FOLDER + '/' + song_name + '/' + stem for stem in listdir(STEM_FOLDER + "/" + song_name)]

            # Render template with stem audio
            return render_template("player.html", stems=stems) 
        
        # Make stems
        else: 
            # New directory for song's stems
            #new_folder = join(STEM_FOLDER, song_name)
            
            # Make a directory for the song's stems
            #os.mkdir(new_folder)
            
            # Spleet the song. TODO: PLEASE CHECK that this works (it should put stems in the stem folder)
            os.system("spleeter separate {} -p spleeter:5stems -o {}".format(song_path, STEM_FOLDER))

            # Create list of stems
            stems = [STEM_FOLDER + '/' + song_name + '/' + stem for stem in listdir(STEM_FOLDER + "/" + song_name)]

            # add the songs
            #songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

            return render_template("player.html", stems=stems)

# Pitch shifter
@app.route('/shifter', methods=['GET', 'POST'])
@login_required
def shifter():
    if request.method == 'POST':
        
        # TODO: Alert the user that this may take a minute
        
        # TODO: stop the user from spleeting if a stem directory already exists. or at least do something that stops this from trying to make 2 folders with the same name.
        
        # Get song file path
        song = request.form.get('song')
        
        # Isolate song name
        song_name = song.rsplit('.', 1)[0] # TODO write better code

        # Create song path
        song_path = join(STEM_FOLDER, song_name)

        # If folder exists, stems already exist
        if song_name in [song for song in listdir(PITCHED_FOLDER)]:

            # Generate a list of stem paths
            stems = [PITCHED_FOLDER + '/' + song_name + '/' + stem for stem in listdir(PITCHED_FOLDER + "/" + song_name)]

            # Render template with stem audio
            return render_template("player.html", stems=stems) 
        
        # New directory for song's stems
        pitched_folder = 'static/pitched/' + song_name

        # Paths for current stems and pitched stems
        current_vocals = song_path + '/vocals.wav'
        current_bass = song_path + '/bass.wav'
        current_other = song_path + '/other.wav'
        current_piano = song_path + '/piano.wav'
        current_drums = song_path + '/drums.wav'
        
        shift_vocals = pitched_folder + '/vocals.wav'
        shift_bass = pitched_folder + '/bass.wav'
        shift_other = pitched_folder + '/other.wav'
        shift_piano = pitched_folder + '/piano.wav'
        shift_drums = pitched_folder + '/drums.wav'

        #TODO only let the pitch work if song is already spleeted
        
        #TODO add a blending feature also to blend in background vocals

        # Make folder for the new pitched stems
        os.mkdir(pitched_folder)

        # Spleet the song. TODO: PLEASE CHECK that this works (it should put stems in the stem folder)
        os.system("pitchshifter -s {} -o {} -p 1 -b 1".format(current_vocals,shift_vocals))
        os.system("pitchshifter -s {} -o {} -p 1 -b 1".format(current_bass,shift_bass))
        os.system("pitchshifter -s {} -o {} -p 1 -b 1".format(current_other,shift_other))
        os.system("pitchshifter -s {} -o {} -p 1 -b 1".format(current_piano,shift_piano))
        os.system("pitchshifter -s {} -o {} -p 1 -b 1".format(current_drums,shift_drums))

        # Create list of stems. TODO: if spleeter works double check which file it sends the stems to. (it might send them to an 'output' folder under the new_folder)
        pitched_stems = [PITCHED_FOLDER + '/' + song_name + '/' + stem for stem in listdir(PITCHED_FOLDER + "/" + song_name)]

        return render_template("player.html", stems=pitched_stems)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username") or not request.form.get("password"):
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Forget any user_id
        session.clear()

        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username.")
            return redirect("/register")

        # Ensure username is not duplicate
        if db.execute("SELECT * FROM users WHERE username=?", request.form.get("username")):
            flash("Username is already taken.")
            return redirect("/register")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Must provide password.")
            return redirect("/register")
        # Ensure password was submitted
        if request.form.get("password").isalpha():
            flash("Password cannot contain only letters.")
            return redirect("/register")

        # Passwords do not match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match.")
            return redirect("/register")

        # Insert into database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()