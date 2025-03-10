
<script>

var stalling = []

function collect_stalling(what) {
    var video = document.getElementById("stimuli");
    stall_event = {
        "media_time": video.currentTime,
        "start_timestamp": Date.now(),
        "what": what,
    };
    stalling.push(stall_event);
}

function video_ended() {
    var video = document.getElementById("stimuli");
    var qmeta = video.getVideoPlaybackQuality();

    qmeta_json = {
        "droppedVideoFrames": qmeta.droppedVideoFrames,
        "totalVideoFrames": qmeta.totalVideoFrames,
        "stalling_events": stalling
    }
    document.getElementById("quality_meta").value = JSON.stringify(qmeta_json);
    //console.log(qmeta_json);
}

function store_window_size() {
    var h = window.innerHeight;
    var w = window.innerWidth;
    document.getElementById("ww").value = w;
    document.getElementById("wh").value = h;

    // store zoom factor (see https://stackoverflow.com/a/45191169)
    document.getElementById("wz").value =  window.devicePixelRatio;

}

function image_loaded() {
    console.log("image here");
    store_window_size();

    document.getElementById("pi").value ++;
    document.getElementById("info").style.display = "none";
    document.getElementById("playbutton").style.display = "none";
    document.getElementById("loader").style.display = "none";
    stimuli_loaded = true;
}

function play() {

    var stimuli = document.getElementById("stimuli");
    /* no full screen
    if (stimuli.tagName != "AUDIO") {
        stimuli.requestFullscreen();
    }
    // hiding of the video/audio element
    document.getElementById("stimuli").style.display = "inline";
    */
    stimuli.play();
    store_window_size();

    console.log("hide button");
    document.getElementById("playbutton").style.display = "none";
    document.getElementById("info").style.display = "inline";
    document.getElementById("pi").value ++;
}

var stimuli_loaded = false;

function display_button() {
    console.log("here we go");
    if (!stimuli_loaded) { // while pressing the button several times this event was fired again thus this will prevent this behaviour
        document.getElementById("loader").style.display = "none";
        //document.getElementById("stimuli").style.display = "inline";
        document.getElementById("playbutton").style.display = "inline";
    }
    stimuli_loaded = true;

}

function hide_media_element() {

    document.getElementById("playbutton").style.display = "inline";
    document.getElementById("info").style.display = "none";
    return; // we dont hide it.. only required for fullscreen
    var stimuli = document.getElementById("stimuli");
    if (stimuli.tagName != "AUDIO") {
        document.exitFullscreen();
    }
    stimuli.style.display = "none";
    document.getElementById("info").style.display = "none";
}
</script>
