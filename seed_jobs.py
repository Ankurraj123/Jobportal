"""
Seed script: create employer account + add 3 jobs per category.
Run: python seed_jobs.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
django.setup()

from account.models import User
from jobapp.models import Category, Job

# ── 1. Create / get employer ──────────────────────────────────────────────────
email = 'ankue2005@gmail.com'
password = '@RAJ2529'

user, created = User.objects.get_or_create(
    email=email,
    defaults={
        'first_name': 'Ankur Enterprises',
        'last_name': 'Corp',
        'role': 'employer',
        'gender': 'M',
        'is_active': True,
    }
)
if created:
    user.set_password(password)
    user.save()
    print(f'Created employer: {email}')
else:
    # Make sure it's an employer
    if user.role != 'employer':
        user.role = 'employer'
        user.save()
    print(f'Employer already exists: {email}')

# ── 2. Jobs data per category ─────────────────────────────────────────────────
jobs_data = {
    'Software Development': [
        {
            'title': 'Senior Django Developer',
            'description': '<p>We are looking for a skilled Django developer to join our backend team. You will design, build, and maintain efficient, reusable Python code and integration with various back-end services.</p><p><b>Requirements:</b> 3+ years of Django experience, REST API design, PostgreSQL, Git.</p>',
            'salary': '$90,000 – $120,000',
            'location': 'Remote',
            'job_type': '1',
            'last_date': '2025-06-30',
        },
        {
            'title': 'React Frontend Engineer',
            'description': '<p>Join our product team to build beautiful, performant user interfaces using React and TypeScript. Collaborate with designers and backend engineers.</p><p><b>Requirements:</b> 2+ years React, TypeScript, REST APIs, CSS-in-JS.</p>',
            'salary': '$80,000 – $110,000',
            'location': 'New York, NY',
            'job_type': '1',
            'last_date': '2025-06-30',
        },
        {
            'title': 'DevOps Intern',
            'description': '<p>Exciting internship opportunity to work with our infrastructure team. You will assist in managing CI/CD pipelines, Docker, and Kubernetes deployments.</p><p><b>Requirements:</b> Basic Linux knowledge, Python scripting, interest in cloud platforms.</p>',
            'salary': '$2,000/month',
            'location': 'Austin, TX',
            'job_type': '3',
            'last_date': '2025-06-15',
        },
    ],
    'Marketing': [
        {
            'title': 'Digital Marketing Manager',
            'description': '<p>Lead our digital marketing efforts across SEO, SEM, email, and social media channels. Own the full marketing funnel from awareness to conversion.</p><p><b>Requirements:</b> 4+ years digital marketing, Google Analytics, HubSpot, strong copywriting.</p>',
            'salary': '$70,000 – $95,000',
            'location': 'Chicago, IL',
            'job_type': '1',
            'last_date': '2025-07-01',
        },
        {
            'title': 'Social Media Specialist',
            'description': '<p>Manage and grow our brand presence across Instagram, LinkedIn, Twitter, and TikTok. Create engaging content and run paid campaigns.</p><p><b>Requirements:</b> 2+ years social media management, content creation, analytics tools.</p>',
            'salary': '$45,000 – $60,000',
            'location': 'Los Angeles, CA',
            'job_type': '1',
            'last_date': '2025-07-15',
        },
        {
            'title': 'Content Marketing Intern',
            'description': '<p>Support our content team in writing blog posts, case studies, and email campaigns. Great opportunity to build your marketing career.</p><p><b>Requirements:</b> Strong writing skills, basic SEO knowledge, passion for storytelling.</p>',
            'salary': '$1,500/month',
            'location': 'Remote',
            'job_type': '3',
            'last_date': '2025-06-20',
        },
    ],
    'Design': [
        {
            'title': 'Senior UI/UX Designer',
            'description': '<p>We are seeking a creative Senior UI/UX Designer to create amazing user experiences. You will work closely with product managers and developers to balance user needs with business goals.</p><p><b>Requirements:</b> 4+ years UI/UX, Figma, user research, design systems.</p>',
            'salary': '$85,000 – $115,000',
            'location': 'San Francisco, CA',
            'job_type': '1',
            'last_date': '2025-07-10',
        },
        {
            'title': 'Graphic Designer',
            'description': '<p>Create compelling visual assets for digital and print. Work on brand identity, marketing materials, social media assets, and product illustrations.</p><p><b>Requirements:</b> 2+ years graphic design, Adobe Creative Suite, strong portfolio.</p>',
            'salary': '$50,000 – $70,000',
            'location': 'Remote',
            'job_type': '2',
            'last_date': '2025-07-01',
        },
        {
            'title': 'Design Intern',
            'description': '<p>Assist our design team with wireframing, prototyping, and visual design tasks. Learn from experienced designers in a fast-paced startup environment.</p><p><b>Requirements:</b> Figma or Sketch basics, eye for design, portfolio/design coursework.</p>',
            'salary': '$1,800/month',
            'location': 'Seattle, WA',
            'job_type': '3',
            'last_date': '2025-06-25',
        },
    ],
    'Data Science': [
        {
            'title': 'Machine Learning Engineer',
            'description': '<p>Design and build machine learning systems and models. Work on NLP, computer vision, and recommendation systems at scale.</p><p><b>Requirements:</b> 3+ years ML, Python, TensorFlow/PyTorch, MLOps, SQL.</p>',
            'salary': '$110,000 – $150,000',
            'location': 'Remote',
            'job_type': '1',
            'last_date': '2025-07-20',
        },
        {
            'title': 'Data Analyst',
            'description': '<p>Analyze large datasets to discover insights that drive business decisions. Build dashboards, reports, and data models for stakeholders.</p><p><b>Requirements:</b> 2+ years SQL, Python or R, Tableau/Power BI, statistical analysis.</p>',
            'salary': '$65,000 – $90,000',
            'location': 'Boston, MA',
            'job_type': '1',
            'last_date': '2025-07-01',
        },
        {
            'title': 'Data Science Intern',
            'description': '<p>Work alongside our data science team on real-world ML problems. Gain hands-on experience with data pipelines, model training, and evaluation.</p><p><b>Requirements:</b> Python, pandas, numpy, statistics coursework, curiosity.</p>',
            'salary': '$2,200/month',
            'location': 'New York, NY',
            'job_type': '3',
            'last_date': '2025-06-30',
        },
    ],
    'Sales': [
        {
            'title': 'Enterprise Account Executive',
            'description': '<p>Drive revenue by selling our SaaS platform to enterprise clients. Manage the full sales cycle from prospecting to close.</p><p><b>Requirements:</b> 5+ years B2B SaaS sales, Salesforce CRM, strong negotiation skills.</p>',
            'salary': '$100,000 + commission',
            'location': 'Denver, CO',
            'job_type': '1',
            'last_date': '2025-07-15',
        },
        {
            'title': 'Inside Sales Representative',
            'description': '<p>Contact prospects, qualify leads, and schedule demos for our Account Executives. Grow into a closing role with time.</p><p><b>Requirements:</b> 1+ year sales experience, excellent communication, CRM familiarity.</p>',
            'salary': '$45,000 + OTE $70,000',
            'location': 'Remote',
            'job_type': '1',
            'last_date': '2025-07-10',
        },
        {
            'title': 'Sales Intern',
            'description': '<p>Support our sales team with lead research, outreach, and CRM management. Learn the fundamentals of B2B SaaS sales from experienced reps.</p><p><b>Requirements:</b> Strong communication skills, interest in tech sales, organised.</p>',
            'salary': '$1,600/month',
            'location': 'Chicago, IL',
            'job_type': '3',
            'last_date': '2025-06-20',
        },
    ],
}

# ── 3. Seed jobs ──────────────────────────────────────────────────────────────
total_created = 0
for cat_name, jobs in jobs_data.items():
    try:
        cat = Category.objects.get(name=cat_name)
    except Category.DoesNotExist:
        print(f'Category "{cat_name}" not found, skipping.')
        continue

    for j in jobs:
        job, created = Job.objects.get_or_create(
            title=j['title'],
            user=user,
            defaults={
                'description': j['description'],
                'salary': j['salary'],
                'location': j['location'],
                'job_type': j['job_type'],
                'category': cat,
                'company_name': 'Ankur Enterprises',
                'last_date': j['last_date'],
                'is_published': True,
                'is_closed': False,
                'company_description': '<p>Ankur Enterprises is a forward-thinking technology company hiring top talent across departments.</p>',
                'url': 'https://example.com',
            }
        )
        if created:
            total_created += 1
            print(f'  ✅ Created: [{cat_name}] {job.title}')
        else:
            print(f'  ⚠️  Already exists: [{cat_name}] {job.title}')

print(f'\nDone! {total_created} new jobs created.')
