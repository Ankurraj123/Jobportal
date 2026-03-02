content = """\
{% extends 'base.html' %}
{% load static %}
{% block title %}My Profile \u2014 JobPortal{% endblock %}

{% block content %}
<div style="background:linear-gradient(135deg,var(--accent),#7c3aed); padding:40px 0 80px;">
    <div class="container" style="position:relative;z-index:1;">
        <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">
            <div style="width:90px;height:90px;border-radius:50%;background:rgba(255,255,255,0.2);backdrop-filter:blur(10px);border:3px solid rgba(255,255,255,0.4);display:flex;align-items:center;justify-content:center;font-size:2.2rem;font-weight:800;color:#fff;flex-shrink:0;">
                {{ profile_user.first_name|slice:":1"|upper|default:"?" }}
            </div>
            <div>
                <h1 style="color:#fff;font-size:1.8rem;font-weight:800;margin-bottom:4px;">
                    {{ profile_user.get_full_name|default:profile_user.email }}
                </h1>
                <p style="color:rgba(255,255,255,0.8);margin-bottom:8px;">{{ profile_user.email }}</p>
                {% if cv_links %}
                <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
                    {% if cv_links.linkedin %}<a href="{{ cv_links.linkedin }}" target="_blank" style="background:rgba(255,255,255,0.2);color:#fff;padding:4px 12px;border-radius:20px;font-size:0.78rem;font-weight:600;text-decoration:none;">LinkedIn</a>{% endif %}
                    {% if cv_links.github %}<a href="{{ cv_links.github }}" target="_blank" style="background:rgba(255,255,255,0.2);color:#fff;padding:4px 12px;border-radius:20px;font-size:0.78rem;font-weight:600;text-decoration:none;">GitHub</a>{% endif %}
                    {% if cv_links.phone %}<span style="background:rgba(255,255,255,0.2);color:#fff;padding:4px 12px;border-radius:20px;font-size:0.78rem;font-weight:600;">{{ cv_links.phone }}</span>{% endif %}
                </div>
                {% endif %}
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <span style="background:rgba(255,255,255,0.2);color:#fff;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;">
                        {% if profile_user.role == 'employee' %}Employee{% else %}Employer{% endif %}
                    </span>
                    <span style="background:{% if profile_user.is_active %}rgba(16,185,129,0.3){% else %}rgba(239,68,68,0.3){% endif %};color:#fff;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;">
                        {% if profile_user.is_active %}Active{% else %}Inactive{% endif %}
                    </span>
                </div>
            </div>
            <div style="margin-left:auto;">
                {% if profile_user.role == 'employee' %}
                <a href="{% url 'account:edit-profile' profile_user.id %}" class="jp-btn jp-btn-primary" style="background:rgba(255,255,255,0.2);border:1.5px solid rgba(255,255,255,0.5);">Edit Profile</a>
                {% endif %}
            </div>
        </div>
    </div>
</div>

<div class="container" style="margin-top:-40px; position:relative; z-index:2; padding-bottom:60px;">
    <div class="row">
        <!-- LEFT SIDEBAR -->
        <div class="col-md-4" style="padding:6px; margin-bottom:16px;">
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:16px;">Basic Info</h5>
                <table style="width:100%;font-size:0.875rem;">
                    {% if profile_user.gender %}
                    <tr>
                        <td style="padding:8px 0;color:var(--text-muted);width:110px;">Gender</td>
                        <td style="font-weight:500;">{{ profile_user.get_gender_display }}</td>
                    </tr>
                    {% endif %}
                    <tr>
                        <td style="padding:8px 0;color:var(--text-muted);">Member Since</td>
                        <td style="font-weight:500;">{{ profile_user.date_joined|date:"d M Y" }}</td>
                    </tr>
                    <tr>
                        <td style="padding:8px 0;color:var(--text-muted);">Last Login</td>
                        <td style="font-weight:500;">{{ profile_user.last_login|date:"d M Y H:i"|default:"\u2014" }}</td>
                    </tr>
                </table>
            </div>

            {% if profile_user.role == 'employee' %}
            {% if profile_user.bio %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:12px;">About Me</h5>
                <p style="font-size:0.875rem;color:var(--text-secondary);line-height:1.7;margin:0;">{{ profile_user.bio }}</p>
            </div>
            {% endif %}

            {% if skills_list %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:12px;">Skills</h5>
                <div style="display:flex;flex-wrap:wrap;gap:6px;">
                    {% for skill in skills_list %}
                    <span style="padding:4px 12px;background:var(--accent-light);color:var(--accent);border-radius:20px;font-size:0.78rem;font-weight:600;">{{ skill }}</span>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% if cv_certificates %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:12px;">Certificates</h5>
                <ul style="list-style:none;padding:0;margin:0;">
                    {% for cert in cv_certificates %}
                    <li style="padding:6px 0;border-bottom:1px solid var(--border-color);font-size:0.85rem;">{{ cert }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}

            {% if cv_achievements %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:12px;">Achievements</h5>
                <ul style="list-style:none;padding:0;margin:0;">
                    {% for ach in cv_achievements %}
                    <li style="padding:6px 0;border-bottom:1px solid var(--border-color);font-size:0.85rem;">{{ ach }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}

            {% if profile_user.resume %}
            <div class="jp-card">
                <h5 style="font-weight:700;margin-bottom:12px;">Resume / CV</h5>
                <a href="{{ profile_user.resume.url }}" target="_blank" class="jp-btn jp-btn-primary" style="width:100%;justify-content:center;">Download CV</a>
            </div>
            {% endif %}
            {% endif %}
        </div>

        <!-- RIGHT MAIN CONTENT -->
        <div class="col-md-8" style="padding:6px;">
            {% if profile_user.role == 'employee' %}

            {% if profile_user.education %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:16px;">Education</h5>
                <p style="font-size:0.875rem;color:var(--text-secondary);line-height:1.7;">{{ profile_user.education|linebreaksbr }}</p>
            </div>
            {% endif %}

            {% if profile_user.experience %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:16px;">Experience</h5>
                <p style="font-size:0.875rem;color:var(--text-secondary);line-height:1.7;">{{ profile_user.experience|linebreaksbr }}</p>
            </div>
            {% endif %}

            {% if cv_projects %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:16px;">Projects</h5>
                <div style="display:flex;flex-direction:column;gap:16px;">
                    {% for proj in cv_projects %}
                    <div style="border:1px solid var(--border-color);border-radius:12px;padding:16px;background:var(--bg-secondary,#f8f9fa);">
                        <div style="font-weight:700;font-size:0.95rem;color:var(--text-primary);margin-bottom:6px;">{{ proj.title }}</div>
                        {% if proj.description %}<p style="font-size:0.85rem;color:var(--text-secondary);line-height:1.6;margin-bottom:8px;">{{ proj.description }}</p>{% endif %}
                        {% if proj.tech %}<div style="font-size:0.78rem;color:var(--accent);font-weight:600;background:var(--accent-light);display:inline-block;padding:2px 10px;border-radius:20px;">{{ proj.tech }}</div>{% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% if cv_training %}
            <div class="jp-card" style="margin-bottom:16px;">
                <h5 style="font-weight:700;margin-bottom:16px;">Training &amp; Courses</h5>
                <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:8px;">
                    {% for t in cv_training %}
                    <li style="display:flex;gap:10px;align-items:flex-start;font-size:0.875rem;color:var(--text-secondary);">{{ t }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}

            <div class="jp-card">
                <h5 style="font-weight:700;margin-bottom:16px;">My Applications ({{ applications|length }})</h5>
                {% if applications %}
                <div style="display:flex;flex-direction:column;gap:10px;">
                    {% for app in applications %}
                    <a href="{% url 'jobapp:single-job' app.job.id %}" style="text-decoration:none;">
                        <div class="jp-job-card" style="display:flex;padding:14px 18px;">
                            <div class="jp-job-logo" style="width:44px;height:44px;font-size:0.9rem;">{{ app.job.company_name|slice:":2"|upper }}</div>
                            <div class="jp-job-body">
                                <div class="jp-job-title">{{ app.job.title }}</div>
                                <div class="jp-job-company">{{ app.job.company_name }}</div>
                            </div>
                            <div style="flex-shrink:0;align-self:center;text-align:right;">
                                {% if app.status == 'accepted' %}<span class="jp-badge jp-badge-success">Accepted</span>
                                {% elif app.status == 'rejected' %}<span class="jp-badge jp-badge-danger">Rejected</span>
                                {% else %}<span class="jp-badge" style="background:rgba(245,158,11,0.12);color:var(--warning);">Pending</span>{% endif %}
                                <div style="font-size:0.75rem;color:var(--text-muted);margin-top:4px;">{{ app.timestamp|date:"d M Y" }}</div>
                            </div>
                        </div>
                    </a>
                    {% endfor %}
                </div>
                {% else %}
                <div style="text-align:center;padding:40px 0;">
                    <p style="color:var(--text-muted);">You haven't applied to any jobs yet.</p>
                    <a href="{% url 'jobapp:job-list' %}" class="jp-btn jp-btn-primary" style="margin-top:12px;display:inline-flex;">Browse Jobs</a>
                </div>
                {% endif %}
            </div>

            {% else %}
            <!-- EMPLOYER -->
            <div class="jp-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;">
                    <h5 style="font-weight:700;margin:0;">Posted Jobs ({{ posted_jobs|length }})</h5>
                    <a href="{% url 'jobapp:create-job' %}" class="jp-btn jp-btn-primary" style="padding:7px 16px;font-size:0.8rem;">+ Post New Job</a>
                </div>
                {% if posted_jobs %}
                <table class="jp-table">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Type</th>
                            <th>Posted</th>
                            <th>Applicants</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for job in posted_jobs %}
                        <tr>
                            <td><a href="{% url 'jobapp:single-job' job.id %}" style="font-weight:600;">{{ job.title }}</a></td>
                            <td>
                                {% if job.job_type == '1' %}<span class="jp-badge jp-badge-success">Full Time</span>
                                {% elif job.job_type == '2' %}<span class="jp-badge jp-badge-danger">Part Time</span>
                                {% else %}<span class="jp-badge jp-badge-info">Internship</span>{% endif %}
                            </td>
                            <td style="color:var(--text-muted);font-size:0.8rem;">{{ job.timestamp|date:"d M Y" }}</td>
                            <td>
                                {% if job.applicant_count %}
                                <a href="{% url 'jobapp:applicants' job.id %}" style="display:inline-flex;align-items:center;gap:6px;font-weight:700;text-decoration:none;color:var(--accent);">
                                    <span style="background:var(--accent-light);color:var(--accent);padding:3px 12px;border-radius:20px;font-size:0.82rem;font-weight:700;">
                                        {{ job.applicant_count }} Applied
                                    </span>
                                </a>
                                {% else %}
                                <span style="color:var(--text-muted);font-size:0.8rem;">No applicants yet</span>
                                {% endif %}
                            </td>
                            <td>
                                {% if not job.is_published %}<span class="jp-badge" style="background:rgba(245,158,11,0.12);color:var(--warning);">Pending</span>
                                {% elif job.is_closed %}<span class="jp-badge jp-badge-danger">Closed</span>
                                {% else %}<span class="jp-badge jp-badge-success">Active</span>{% endif %}
                            </td>
                            <td><a href="{% url 'jobapp:edit-job' job.id %}" class="jp-btn" style="padding:3px 10px;font-size:0.75rem;background:var(--accent-light);color:var(--accent);">Edit</a></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <div style="text-align:center;padding:40px 0;">
                    <p style="color:var(--text-muted);">You haven't posted any jobs yet.</p>
                    <a href="{% url 'jobapp:create-job' %}" class="jp-btn jp-btn-primary" style="margin-top:12px;display:inline-flex;">Post a Job</a>
                </div>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
"""

with open(r'template\account\profile.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Written OK -", len(content), "chars")
