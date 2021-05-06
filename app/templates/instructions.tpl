% rebase('templates/skeleton.tpl', title=title)

<h1 class="mt-5">Instructions</h1>

<div id="screensize_error" class="alert alert-danger" style="display:none">
    Your browser window is not large enough, please maximize your window.
</div>

<p>
You will see differently encoded videos.
The task will then be to evaluate the quality of the shown videos.
The videos have a duration of 10-15 seconds.
</p>
<p>
The training phase comprises shows you the rating scheme and the general interface.
</p>


<div class="alert alert-secondary" role="alert">
Please answer as intuitive as possible. There are no right or wrong answers.
</div>
<div class="alert alert-secondary" role="alert">
Please maximize your browser window.
</div>

<p>
<a class="btn btn-large btn-success" href="/training/0" onclick="check_screensize(event)"  id="next">next</a>
</p>



% include("templates/precache.tpl", stimuli=stimuli)
