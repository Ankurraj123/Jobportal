content = """\
<!-- NAVBAR -->
<nav class="jp-navbar">
  <div class="container-fluid">

    <a href="{% url 'jobapp:home' %}" class="jp-logo">&#128188; JobPortal</a>

    <ul class="jp-nav-links jp-nav-desktop" style="margin:0;">
      <li><a href="{% url 'jobapp:home' %}" {% if request.resolver_match.url_name == 'home' %}class="active"{% endif %}>Home</a></li>
      <li><a href="{% url 'jobapp:job-list' %}" {% if request.resolver_match.url_name == 'job-list' %}class="active"{% endif %}>Find Jobs</a></li>

      {% if user.is_superuser %}
      <li>
        <a href="{% url 'admin_panel:dashboard' %}" class="jp-btn jp-btn-outline" style="font-size:0.8rem;padding:6px 14px;">
          Admin Panel
        </a>
      </li>
      {% endif %}

      {% if user.is_authenticated %}
      {% if user.role == 'employer' %}
      <li><a href="{% url 'jobapp:create-job' %}" {% if request.resolver_match.url_name == 'create-job' %}class="active"{% endif %}>Post a Job</a></li>
      {% endif %}

      <li class="jp-dropdown">
        <a style="cursor:pointer;display:flex;align-items:center;gap:8px;">
          <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#a78bfa);display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;color:#fff;flex-shrink:0;">
            {% if user.first_name %}{{ user.first_name|slice:":1"|upper }}{% else %}{{ user.email|slice:":1"|upper }}{% endif %}
          </div>
          <span>{% if user.first_name %}{{ user.first_name }}{% else %}Account{% endif %} &#9662;</span>
        </a>

        <div class="jp-dropdown-menu" style="min-width:230px;">
          <div style="padding:12px 14px 10px;border-bottom:1px solid var(--border-color);margin-bottom:4px;">
            <div style="font-weight:700;font-size:0.9rem;color:var(--text-primary);">
              {% if user.first_name %}{{ user.first_name }} {{ user.last_name }}{% else %}{{ user.email }}{% endif %}
            </div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:2px;">{{ user.email }}</div>
            {% if user.role == 'employer' %}
            <span style="display:inline-block;margin-top:6px;font-size:0.7rem;font-weight:600;padding:2px 10px;border-radius:20px;background:var(--accent-light);color:var(--accent);">Employer</span>
            {% else %}
            <span style="display:inline-block;margin-top:6px;font-size:0.7rem;font-weight:600;padding:2px 10px;border-radius:20px;background:rgba(16,185,129,0.12);color:var(--success);">Employee</span>
            {% endif %}
          </div>

          <a href="{% url 'account:profile' %}">My Profile</a>
          <a href="{% url 'jobapp:dashboard' %}">Dashboard</a>
          {% if user.role == 'employee' %}
          <a href="{% url 'account:edit-profile' request.user.id %}">Edit Profile</a>
          {% endif %}
          <div style="height:1px;background:var(--border-color);margin:4px 0;"></div>
          <a href="{% url 'account:logout' %}" style="color:var(--danger)!important;">Logout</a>
        </div>
      </li>

      {% else %}
      <li class="jp-dropdown">
        <a style="cursor:pointer;">Register &#9662;</a>
        <div class="jp-dropdown-menu">
          <a href="{% url 'account:employer-registration' %}">As Employer</a>
          <a href="{% url 'account:employee-registration' %}">As Employee</a>
        </div>
      </li>
      <li><a href="{% url 'account:login' %}" {% if request.resolver_match.url_name == 'login' %}class="active"{% endif %}>Login</a></li>
      {% endif %}
    </ul>

    <div style="display:flex;align-items:center;gap:10px;">
      <button class="theme-toggle-btn" id="jp-theme-toggle" title="Toggle theme">
        <span id="jp-sun" style="display:none;">&#9728;</span>
        <span id="jp-moon">&#127769;</span>
      </button>
      <button class="mobile-menu-toggle" id="jp-menu-toggle" aria-label="Open menu">&#9776;</button>
    </div>

  </div>
</nav>
"""

with open(r'template\header.html', 'w', encoding='utf-8') as f:
    f.write(content)

# verify
with open(r'template\header.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Written {len(lines)} lines.")
print(lines[7].rstrip())
print(lines[8].rstrip())
