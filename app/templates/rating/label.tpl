
<div class="col-12" id="ratingform" >

% is_audio = stimuli_file.split(".")[-1].lower() in ["wav", "flac", "ogg", "aac", "mp3", "opus"]
% is_image = stimuli_file.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif", "tiff"]
% is_video = not is_audio and not is_image



<h5>Please check whether the image follows the listed photo rules.</h5>



  % route = f"save_rating?stimuli_idx={stimuli_idx}" if not train else "training/" + str(stimuli_idx + 1)
  <form id="form1" action="/{{route}}" method="post">

    <%
      labels = [
        {"value":"dog", "text": "there is a dog"},
        {"value":"cat", "text": "there is a cat"}

      ]
    %>

    <!--<div class="funkyradio">-->
    <div class="funkyradio-success">
      % for label in labels:


          <div class="form-check form-switch">
            <input class="form-check-input" type="checkbox" id="switch_{{label['value']}}" name="switch_{{label['value']}}" value="yes">
            <label class="form-check-label" for="switch_{{label['value']}}">{{label['text']}}</label>
          </div>

      % end
    </div>


    <input type="hidden" value="{{stimuli_file}}" id="stimuli_file" name="stimuli_file" />
    <input type="hidden" value="{{stimuli_idx}}" id="stimuli_idx" name="stimuli_idx" />
    <input type="hidden" value="-1" id="ww" name="ww" />
    <input type="hidden" value="-1" id="wh" name="wh" />
    <input type="hidden" value="0" id="pi" name="pi" />


    <button type="submit" id="submitButton" class="btn btn-success btn-block" onclick="check_form(event)">submit</button>
    % if dev:
      <button type="submit" class="btn btn-success" formnovalidate>skip (for dev)</button>
    % end

    <div id="playonce" class="btn alert-danger" style="display:none;cursor:default; margin-top: 0.5em; margin-bottom: 0.5em" disabled>Please play the stimuli at least once.</div>
    <div id="ratingselect" class="btn alert-danger" style="display:none;cursor:default; margin-top: 0.5em; margin-bottom: 0.5em" disabled>Please select a rating.</div>
  </form>
</div>



<script>

    function display_rating(){
      document.getElementById("ratingform").style.display="block";
    }

    function check_form(event) {
      console.log(document.getElementById("pi").value);
      document.getElementById("playonce").style.display = "none";
      document.getElementById("ratingselect").style.display = "none";

      if (document.getElementById("pi").value == 0) {
          document.getElementById("playonce").style.display="block";
          event.preventDefault();
          return
      }
    }
</script>