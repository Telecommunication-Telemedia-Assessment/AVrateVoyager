
<script>
  var loaded_files = 0;
  function loaded(i) {
      console.log("loaded");
      loaded_files ++;
  }

</script>
<div>
  % for x in stimuli:
    <link class="file" rel="prefetch" href="{{x.replace("./", "/")}}" as="video" onload="loaded(this)">
  % end

</div>