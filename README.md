# Using Flask/Python backend and HTML/JavaScript/CSS frontend to create music splitter and stem player

## Description

THIS README IS OUTDATED - TAKE FROM JOHNS COMPUTER

This website allows a user to upload any song as a MP3 file, separating the song into 5 separate "stems" that represent the vocals, bass, drums, piano, and other instruments of the original file. We have incorporated a tool called Spleeter by Deezer that is able to split a song into its components. For legal reasons (e.g., copyright laws), users can only upload songs that they rightfully own and are allowed to modify. Once the song is separated, users can then play the song and mute certain stems to modify their listening experience. For example, it is possible to mute the vocals during particular moments of the song to create a "karaoke" effect for a large audience of listeners.

## Use cases

There are many applications of this project. For example, users can use the website as their personal "band." They can mute the drums of a track, for instance, and play the drums themselves, allowing them to create a more immersive performance. Similarly, it is possible to isolate just the vocals, allowing music producers to overlay the vocals to new instrumentals. Primarily, we have experimented using the tool in group karaoke settings, in which we have strategically muted the vocals of the song as our own "DJs" in order to immerse ourselves more deeply into the songs. 

## Compatability

The Spleeter tool runs into compatability issues on M1 Macs. However, the functionality should work well on Windows and Intel Macs with the right dependencies.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
Python 3
Flask
Tornado Web Server
```

### Installing basic requirements

Installing dependencies 
```
pip install -r requirements.txt
```
Once all packages are downloaded and installed run.

### Installng the Pitch Shifter

This portion allows us to pitch up songs without changing the speed. Note: Python 3.7+ is required. To install, make sure to follow the steps below:

```
$ git clone https://github.com/cwoodall/pitch-shifter-py.git
$ cd pitch-shifter-py
$ pip install .
```

## Running the tests
```
To run the app, use the "flask run" command. For some systems (mainly Windows systems), it is necessary to run "python app.py" instead.
```
If this runs into issues, running flask run (depending on your system dependencies) will work.
Open up your browser and visit
```
http://localhost:5000

```
