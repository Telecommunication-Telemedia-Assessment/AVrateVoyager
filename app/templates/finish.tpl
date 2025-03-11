% rebase('templates/skeleton.tpl', title=title)

<h1 class="mt-5">You're done :)</h1>
<p >{{text}}</p>

<a class="btn btn-large btn-success" href="/rc"  id="start">Restart (next Participant)</a>

% if feedback:
If you want to give some feedback, you can do it while filling out the following form.
<form id="feedback_form" action="/finish" method="post">

    <div class="form-group" style="padding-top: 1em; padding-bottom: 1em">
        <textarea class="form-control" id="feedback" name="feedback" rows="5" placeholder="Feedback" required></textarea>
        <input type="text" name="user_id" style="display:none" value={{user_id}}>
    </div>

    <button type="submit" id="submitButton" class="btn btn-success btn-block">submit</button>
</form>
% end