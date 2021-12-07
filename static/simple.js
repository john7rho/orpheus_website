function playAudio() {
    var audio1 = document.getElementById('bass');
    var audio2 = document.getElementById('vocals');
    var audio3 = document.getElementById('drums');
    var audio4 = document.getElementById('other');
    var audio5 = document.getElementById('piano');
    audio1.play();
    audio2.play();
    audio3.play();
    audio4.play();
    audio5.play();
}

function stopAudio() {
    var audio1 = document.getElementById('bass');
    var audio2 = document.getElementById('vocals');
    var audio3 = document.getElementById('drums');
    var audio4 = document.getElementById('other');
    var audio5 = document.getElementById('piano');
    audio1.pause();
    audio2.pause();
    audio3.pause();
    audio4.pause();
    audio5.pause();
}

function refreshAudio() {
    var audio1 = document.getElementById('bass');
    var audio2 = document.getElementById('vocals');
    var audio3 = document.getElementById('drums');
    var audio4 = document.getElementById('other');
    var audio5 = document.getElementById('piano');

    audio1.pause();
    audio2.pause();
    audio3.pause();
    audio4.pause();
    audio5.pause();

    audio1.currentTime = 0;
    audio2.currentTime = 0;
    audio3.currentTime = 0;
    audio4.currentTime = 0;
    audio5.currentTime = 0;
}

function pitchUp() {
    var song = document.getElementById('pitched_song');
    var song_name = song.value;
    var audio1 = document.getElementById('bass');
    var audio2 = document.getElementById('vocals');
    var audio3 = document.getElementById('drums');
    var audio4 = document.getElementById('other');
    var audio5 = document.getElementById('piano');
    audio1.src = "/static/pitched/" + song_name.split('.')[0] + "/bass.wav";
    audio2.src = "/static/pitched/" + song_name.split('.')[0] + "/vocals.wav";
    audio3.src = "/static/pitched/" + song_name.split('.')[0] + "/drums.wav";
    audio4.src = "/static/pitched/" + song_name.split('.')[0] + "/other.wav";
    audio5.src = "/static/pitched/" + song_name.split('.')[0] + "/piano.wav";
    audio1.load();
    audio2.load();
    audio3.load();
    audio4.load();
    audio5.load();
}