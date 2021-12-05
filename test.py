<<<<<<< Updated upstream
from flask import Flask, render_template, Response, request, redirect
=======
from flask import Flask, render_template, Response, request, redirect, flash, session
from flask_session import Session
>>>>>>> Stashed changes
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import sys
import os
from os import listdir
from os.path import isfile, join
from cs50 import SQL

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

# Set folder for uploads
UPLOAD_FOLDER = 'static/uploads' # TODO path breaks depending on OS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Upload configurations
app.config['MAX_CONTENT_PATH'] = 1000000000 # bytes (arbitrary for now)
ALLOWED_EXTENSIONS = {'mp3','mp4'} # add to this

# Set folder for stems
STEM_FOLDER = 'static/stems' # TODO path breaks depending on OS - macOS works with single slash
PITCHED_FOLDER = 'static/pitched'

# Get list of all uploaded songs
songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///orpheus.db")


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


# Orpheus homepage
@app.route("/")
def orpheus:
    return render_template("index.html")


# Display the songs that the user has uploaded
@app.route('/mysongs')
@login_required
def show_songs():
    
    # Get songs that the user has uploaded
    pathless_songs = db.execute("SELECT song FROM songs WHERE user_id=?", session["user_id"])
    
    # Check that the user has uploaded songs
    if len(pathless_songs) == 0:
        return render_template("index.html", text="You have not uploaded any songs yet!")

    # Create list of song names
    pathless_songs = pathless_songs[0]["song"]
    
    song_paths = [UPLOAD_FOLDER + "/" + song for song in pathless_songs]

    return render_template("mysongs.html", songs=song_paths)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect("/login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
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

    # User reached route via GET
    if request.method == "GET":
        # Display registration form
        return render_template("register.html")

    # User submitted form via POST
    else:
        # Initialize variable username as user's username input
        username = request.form.get("username")

        # Check if username is blank
        if len(username) == 0:
            flash("Please specify username")
            return redirect("/register")

        # Check if username is already taken
        if len(db.execute("SELECT username FROM users WHERE username=?", username)) != 0:
            flash("Username taken. Please choose different username")
            return redirect("/register")

        # Get password
        password = request.form.get("password")

        # Initialize variable confirmation as user's second password input
        confirmation = request.form.get("confirmation")

        # Personal touch -- password must be 8 chars and include letters, numbers, and symbols
        # Check that password has 8 or more characters
        if len(password) < 8:
            flash("Your password must be 8 characters or longer")
            return redirect("/register")

        # Check that special characters (non letters/numbers) are included
        if password.isalnum():
            flash("Your password must include special characters")
            return redirect("/register")

        # Check that numbers are included
        if not any(char.isdigit() for char in password):
            flash("Your password must include numbers")
            return redirect("/register")

        # Check that letters are included
        if not any(char.isalpha() for char in password):
            flash("Your password must contain letters")
            return redirect("/register")
            
        # Check that passwords match up
        if password != confirmation:
            flash("Passwords do not match")
            return redirect("/register")

        # Create hash of the user's password
        encryption = generate_password_hash(password)

        # Insert user into user table
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, encryption)

        # Log user in
        session["user_id"] = db.execute("SELECT id FROM users WHERE username=?", username)[0]["id"]

        # Redirect user to home page
        return redirect("/")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

<<<<<<< Updated upstream
@app.route('/uploader', methods=['GET', 'POST'])
=======
# Do not allow more than one period in a file's name
def allowed_name(filename):
    return len(filename.split('.')) == 2

# TODO reject song if already uploaded
@app.route('/upload', methods=['GET', 'POST'])
@login_required
>>>>>>> Stashed changes
def upload_file():

    if request.method == 'POST': # TODO: there's no else here. what's up w that?
    
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/upload')
            
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
<<<<<<< Updated upstream
            return redirect('/')
        if file and allowed_file(file.filename):
=======
            return redirect('/upload')
            
        if (allowed_name(file.filename) == False):
            flash('File name must not have period outside of file type extension')
            return redirect('/upload')
            
        if file and allowed_file(file.filename) and allowed_name(file.filename):
>>>>>>> Stashed changes
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Update list of songs
<<<<<<< Updated upstream
            songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]
            return render_template(simple.html, songs=songs)
    return "success!"
=======
            pathless_songs = db.execute("SELECT song FROM songs WHERE user_id=?", session["user_id"])[0]["song"]
            song_paths = [UPLOAD_FOLDER + "/" + song for song in pathless_songs]
>>>>>>> Stashed changes

            return render_template("index.html", songs=song_paths)
            
    else:
        return render_template("upload.html")

# Spleeter
@app.route('/spleeter', methods=['GET', 'POST'])
@login_required
def spleeter():
    if request.method == 'POST':
        
        # TODO: Alert the user that this may take a minute
        
        # TODO: stop the user from spleeting if a stem directory already exists. or at least do something that stops this from trying to make 2 folders with the same name.
        
        # Get song file path
        song = request.form.get('song')
        
        # Correct path to include working directory
        song_path = join(UPLOAD_FOLDER, song)
        
        # Isolate song name
        song_name = song.rsplit('.', 1)[0]
        
        # New directory for song's stems
        new_folder = join(STEM_FOLDER, song_name)
        
        # Make a directory for the song's stems
        os.system(f"mkdir {new_folder}")
        
        # Spleet the song. TODO: PLEASE CHECK that this works (it should put stems in the stem folder)
        os.system(f"spleeter separate -i {song_path} -p spleeter:2stems -o {new_folder}")

        # Create list of stems. TODO: if spleeter works double check which file it sends the stems to. (it might send them to an 'output' folder under the new_folder)
        stems = [f for f in listdir(new_folder) if isfile(join(new_folder, f))]
        
        # testing
        test = [song_path]

<<<<<<< Updated upstream
=======
        # add the songs
        songs = [f for f in listdir(UPLOAD_FOLDER) if isfile(join(UPLOAD_FOLDER, f))]

        return render_template("simple.html", songs=songs, stems=stems)

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
>>>>>>> Stashed changes

        return render_template("simple.html", songs=songs, stems=test)


#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    

