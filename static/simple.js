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