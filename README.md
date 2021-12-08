# Orpheus
 
## Description
 
Orpheus is a music splitter and stem player built using a Python Flask and SQL backend as well as an HTML/JS/CSS frontend. This website allows a user to upload any song as a MP3 file, separating it into 5 separate “stems” that represent the vocals, bass, drums, piano, and other audio sources in the original file. Orpheus uses the Spleeter API by Deezer to split a song into its components. Due to copyright laws, users can only upload songs that they rightfully own and are allowed to modify. Once the song is separated, users can then play the song and modify the volume of certain stems to modify their listening experience. For example, it is possible to mute the vocals during particular moments of the song to create a karaoke effect for a large audience of listeners. Users can also pitch their songs up a semitone to further alter the song to their liking.
 
## Use cases
 
There are many applications of this project, especially in empowering users to be their own DJs, music producers, and more. For example, users can use the website as their personal band. They can mute the drums of a track, for instance, and play the drums themselves, allowing them to create a more immersive performance. Similarly, it is possible to isolate just the vocals, allowing music producers to overlay the vocals of the song to new instrumentals. It is also possible to use Orpheus in group karaoke settings by muting the vocals of the song.
 
## Compatibility
 
Orpheus is compatible on most modern Windows and Intel Macs. However, the Spleeter API Orpheus uses currently runs into compatibility issues on M1 Macs.
 
## Getting Started
 
These instructions will let you download a copy of the project up and running on your local machine for development and testing purposes.
 
### Prerequisites
 
Users will need Python 3 as well as the following dependencies installed.
 
### Installing Dependencies
 
Installing dependencies
 
```
pip install -r requirements.txt
```
 
### Installing the Pitch Shifter
 
The pitch shifter allows us to pitch up songs without changing the speed. Note: Python 3.7+ is required. To install, make sure to follow the steps below:
 
```
$ git clone https://github.com/cwoodall/pitch-shifter-py.git
 
$ cd pitch-shifter-py
 
$ pip install .
 
$ cd ..
```
 
## Running Orpheus
 
To run the app, run `FLASK_APP=app.py` initially to set up the flask app. Then all future executions can be done with the `flask run` command.
 
For Windows computers, it may be necessary to run `python app.py` instead.
 
Once the web server is up and running, open up your browser and visit
 
```
http://localhost:5000
```