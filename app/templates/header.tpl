<header>
  <!-- Fixed navbar -->
  <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">AVrate Voyager</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav ms-auto">
            % if user_id != "":
            <li class="nav-item">
                <span class="nav-link">ID: {{user_id}}</span>
            </li>

            % end

            <li class="nav-item">
                <a class="nav-link" href="/about">About</a>
            </li>
        </ul>

      </div>
    </div>
  </nav>
</header>