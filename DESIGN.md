## Introduction
 
Our vision was to create a tool that could be used as a “stem player.” Essentially, a user could input a single song file and separate it into vocals, drums, bass, piano, and other instruments (each of which is considered a “stem”). We have made a website to facilitate easier distribution of the tool online as we plan to publish the site in the near future. We use a HTML/JS/CSS front-end to build the user interface in addition to a Python Flask backend. We chose a Python backend in order to implement machine learning tools called Deezer Spleeter and Pitch Shifter (which are explained in the Separation and Pitch Shifter). We have further detailed the reasons behind more specific decisions in the following sections, organized by functionality. The website has three primary functions: uploading, separation, and pitching-up songs. They are described as follows:
 
## Registration / Login
 
Users can make accounts (recorded by a SQL database, which takes a username and hashes a password) in order to keep track of their songs. Users cannot access songs that they have not already uploaded to the website, but to save space on our end, we only store a particular song with a certain name one time in order to reduce redundancy. Thus, we are able to keep track of which users have which songs uploaded while also conserving storage. We created a separate registration (register.html) and login (login.html) page for users, and we implemented Flask sessions to keep track of user logins. Moreover, once a user is logged in (if the session is non-empty), we set up the website to show “Log Off” rather than a login page so that the user can exit their session.
 
## Uploading
 
Users are able to upload local music files (made possible by the upload_file) function in app.py) to the website on the Upload page (upload.html). This enables us to then modify these files by separating them into stems or by pitching them upwards. We have a separate page for uploading music, in which users submit a POST request to upload a music file locally to the website. If the file type is allowed (essentially, it has a music file extension like MP3 and does not contain more than one period), then we accept the file and add it to our database. From there, the user can access it under a different page, My Songs.
 
## My Songs
 
To access uploaded songs, we added a My Songs page (mypage.html) where users can navigate. We employed Jinja to iterate through the user’s uploaded songs, and then users are able to see buttons for getting the stems (using Spleeter) and shifting the pitch (using the pitch shifter). From there, users are able to select the buttons (which is an HTML form, chosen because we can pass the names of the songs to the spleeter() function in app.py) based on which behavior they want to access. From there, the pages redirect to the player page (hidden on the navbar, represented by player.html) where the right song stems can be played.
 
## Separation (“Spleeting”)
 
Once their song is uploaded, users can then navigate to the My Songs page (as mentioned). There is a form with a button that can split a song into its stems. We elected to use the Spleeter API as it was the state-of-the-art model for stem separation; the tool was implemented in the /spleeter method in app.py. Spleeter takes advantage of OS commands in order to take a local audio file and then split it up into the five separate stems, which we can then each play using HTML audio components (and from there, we set src to the path of each stem under the right folder). On the front end, we extended a layout while also including audio components that provided controls for each stem (play/pause, volume controls). From there, we added buttons to control all the stems at once (play/pause, refresh audio) that incorporated Javascript (in simple.js) that allowed us to play the song as normal. The stems can then be muted using the volume controls built into HTML to let us modify the listening experience as intended.
 
## Pitch Shifter
 
Similarly to the splitting, users can navigate to the My Songs page and press a button to pitch shift a song. If the song already has stems in the stems folder, then the Pitch Shifter API will be able to shift the individual stems by one semitone, which can then be saved to a “pitched” folder locally. From there, we can pass the directories of the pitched-up stems to the player page (player.html) and redirect the user to that page. From there, as mentioned above in the Separation section, the user can play the song and mute/edit stems as they see fit.

## Deleting Songs

TODO
