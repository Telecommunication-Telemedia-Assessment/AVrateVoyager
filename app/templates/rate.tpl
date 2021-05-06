% rebase('templates/skeleton.tpl', title=title)


<h3 class="mt-5">{{"Training" if get("train", False) else "Rating"}}</h3>




<div class="row">
% include('templates/stimuli.tpl', stimuli_file=stimuli_file)
</div>
<div class="row" style="padding-top: 1em">
% include('templates/' + rating_template, stimuli_idx=stimuli_idx, stimuli_file=stimuli_file, train=get("train", False))
</div>

% include('templates/progress_bar.tpl', stimuli_done=stimuli_done, stimuli_count=stimuli_count)

