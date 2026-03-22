
p = "%"  # using variable to avoid PowerShell eating % chars

def iftag(name):
    return f"{p}{p} if request.resolver_match.url_name == '{name}' {p}{p}"

def endiftag():
    return f"{p}{p} endif {p}{p}"

def urltag(name):
    return f"{p}{p} url '{name}' {p}{p}"

# Build lines individually to avoid line-wrap issues
L = []
L += ["<!-- NAVBAR -->"]
L += [f'<nav class="jp-navbar">']
L += ['  <div class="container-fluid">']
L += ['']
L += [f'    <a href="{{{urltag("jobapp:home")}}}" class="jp-logo">&#128188; JobPortal</a>']
L += ['']
L += ['    <ul class="jp-nav-links jp-nav-desktop" style="margin:0;">']
L += [f'      <li><a href="{{{urltag("jobapp:home")}}}" {{{iftag("home")}}}class="active"{{{endiftag()}}}>Home</a></li>']
L += [f'      <li><a href="{{{urltag("jobapp:job-list")}}}" {{{iftag("job-list")}}}class="active"{{{endiftag()}}}>Find Jobs</a></li>']
L += ['']
L += [f'      {{{p}% if user.is_superuser %{p}}}']
L += ['      <li>']
L += [f'        <a href="{{{urltag("admin_panel:dashboard")}}}" class="jp-btn jp-btn-outline" style="font-size:0.8rem;padding:6px 14px;">Admin Panel</a>']
L += ['      </li>']
L += [f'      {{{p}% endif %{p}}}']
L += ['']
L += [f'      {{{p}% if user.is_authenticated %{p}}}']
L += [f'      {{{p}% if user.role == \'employer\' %{p}}}']
L += [f'      <li><a href="{{{urltag("jobapp:create-job")}}}" {{{iftag("create-job")}}}class="active"{{{endiftag()}}}>Post a Job</a></li>']
L += [f'      {{{p}% endif %{p}}}']
L += ['']
L += ['      <li class="jp-dropdown">']
L += ['        <a style="cursor:pointer;display:flex;align-items:center;gap:8px;">']
L += ['          <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,var(--accent),#a78bfa);display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;color:#fff;flex-shrink:0;">']
L += [f'            {{{p}% if user.first_name %{p}}}{{{{ user.first_name|slice:":1"|upper }}}}{{{p}% else %{p}}}{{{{ user.email|slice:":1"|upper }}}}{{{p}% endif %{p}}}']
L += ['          </div>']
L += [f'          <span>{{{p}% if user.first_name %{p}}}{{{{ user.first_name }}}}{{{p}% else %{p}}}Account{{{p}% endif %{p}}} &#9662;</span>']
L += ['        </a>']
L += ['']
L += ['        <div class="jp-dropdown-menu" style="min-width:230px;">']
L += ['          <div style="padding:12px 14px 10px;border-bottom:1px solid var(--border-color);margin-bottom:4px;">']
L += ['            <div style="font-weight:700;font-size:0.9rem;color:var(--text-primary);">']
L += [f'              {{{p}% if user.first_name %{p}}}{{{{ user.first_name }}}} {{{{ user.last_name }}}}{{{p}% else %{p}}}{{{{ user.email }}}}{{{p}% endif %{p}}}']
L += ['            </div>']
L += ['            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:2px;">{{ user.email }}</div>']
L += [f'            {{{p}% if user.role == \'employer\' %{p}}}']
L += ['            <span style="display:inline-block;margin-top:6px;font-size:0.7rem;font-weight:600;padding:2px 10px;border-radius:20px;background:var(--accent-light);color:var(--accent);">Employer</span>']
L += [f'            {{{p}% else %{p}}}']
L += ['            <span style="display:inline-block;margin-top:6px;font-size:0.7rem;font-weight:600;padding:2px 10px;border-radius:20px;background:rgba(16,185,129,0.12);color:var(--success);">Employee</span>']
L += [f'            {{{p}% endif %{p}}}']
L += ['          </div>']
L += [f'          <a href="{{{urltag("account:profile")}}}">My Profile</a>']
L += [f'          <a href="{{{urltag("jobapp:dashboard")}}}">Dashboard</a>']
L += [f'          {{{p}% if user.role == \'employee\' %{p}}}']
L += [f'          <a href="{{{urltag("account:edit-profile")}}} {{{{ request.user.id }}}}">Edit Profile</a>']
L += [f'          {{{p}% endif %{p}}}']
L += ['          <div style="height:1px;background:var(--border-color);margin:4px 0;"></div>']
L += [f'          <a href="{{{urltag("account:logout")}}}" style="color:var(--danger)!important;">Logout</a>']
L += ['        </div>']
L += ['      </li>']
L += ['']
L += [f'      {{{p}% else %{p}}}']
L += ['      <li class="jp-dropdown">']
L += ['        <a style="cursor:pointer;">Register &#9662;</a>']
L += ['        <div class="jp-dropdown-menu">']
L += [f'          <a href="{{{urltag("account:employer-registration")}}}">As Employer</a>']
L += [f'          <a href="{{{urltag("account:employee-registration")}}}">As Employee</a>']
L += ['        </div>']
L += ['      </li>']
L += [f'      <li><a href="{{{urltag("account:login")}}}" {{{iftag("login")}}}class="active"{{{endiftag()}}}>Login</a></li>']
L += [f'      {{{p}% endif %{p}}}']
L += ['    </ul>']
L += ['']
L += ['    <div style="display:flex;align-items:center;gap:10px;">']
L += ['      <button class="theme-toggle-btn" id="jp-theme-toggle" title="Toggle theme">']
L += ['        <span id="jp-sun" style="display:none;">&#9728;</span>']
L += ['        <span id="jp-moon">&#127769;</span>']
L += ['      </button>']
L += ['      <button class="mobile-menu-toggle" id="jp-menu-toggle" aria-label="Open menu">&#9776;</button>']
L += ['    </div>']
L += ['']
L += ['  </div>']
L += ['</nav>']

content = "\n".join(L)
# Replace the placeholder tags with proper Django template tags
content = content.replace("{% %}", "{% %}")

with open(r"template\header.html", "w", encoding="utf-8") as f:
    f.write(content)

# Verify
with open(r"template\header.html", "r", encoding="utf-8") as f:
    out = f.readlines()
print(f"Written {len(out)} lines")
print("Line 8:", out[7].strip())
print("Line 9:", out[8].strip())
