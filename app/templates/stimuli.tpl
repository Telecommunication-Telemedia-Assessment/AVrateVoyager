

<div class="col-12">
    % is_audio = stimuli_file.split(".")[-1].lower() in ["wav", "flac", "ogg", "aac", "mp3", "opus"]
    % is_image = stimuli_file.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif", "tiff"]
    % is_video = not is_audio and not is_image
    % task_msg = "listen" if is_audio else "watch"

    <div class="row">
        <div class="col-12 align-top">

            % if is_audio:
            <audio id="stimuli" nocontrols onended="display_rating();hide_media_element();" preload="auto" oncanplaythrough="display_button()" style="display:none" oncontextmenu="return false;">
                <source src="{{stimuli_file.replace("./", "/")}}" type="audio/flac">
                Your browser does not support the audio element.
            </audio>
            % end
            % if is_video:
            <video id="stimuli" class="vstimuli col-12 align-top" nocontrols onended="display_rating();hide_media_element();" preload="auto" oncanplaythrough="display_button()" oncontextmenu="return false;">
                <source src="{{stimuli_file.replace("./", "/")}}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            % end
            % if is_image:
            <img id="stimuli" class="col-12 align-top" onload="image_loaded()" src="{{stimuli_file.replace("./", "/")}}" alt="{{stimuli_file.replace("./", "/")}}" >
            % end
        </div>
    </div>


    <div class="row">
        <div class="col-12">

            <div id="info" style="display:none;cursor:default" class="btn alert-success" disabled>
              Please {{task_msg}}
            </div>
            <div id="loader" class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>

            <button style="display:none" class="btn btn-secondary" id="playbutton" onclick="play()">
            play
            </button>
        </div>
    </div>

</div>

<script>
function image_loaded() {
    console.log("image here");
    var h = window.innerHeight;
    var w = window.innerWidth;
    document.getElementById("ww").value = w;
    document.getElementById("wh").value = h;
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
    var h = window.innerHeight;
    var w = window.innerWidth;
    document.getElementById("ww").value = w;
    document.getElementById("wh").value = h;
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
    return; // we dont hide it..
    var stimuli = document.getElementById("stimuli");
    if (stimuli.tagName != "AUDIO") {
        document.exitFullscreen();
    }
    stimuli.style.display = "none";
    document.getElementById("info").style.display = "none";
}
</script>
