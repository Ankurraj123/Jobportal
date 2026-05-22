"""
Seed script: create employer account (ANKURRAJ2005RAJ@gmail.com / Raj@1234) + add 9 jobs.
Run: python seed_employer_jobs.py
"""
import os
import django
from datetime import date, timedelta

# Set MongoDB connection string to point to Atlas database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
os.environ['MONGODB_URI'] = "mongodb+srv://ankur123:ankur%40123@cluster0.lswjemc.mongodb.net/jobportal_db?retryWrites=true&w=majority&appName=Cluster0"

django.setup()

from account.models import User
from jobapp.models import Category, Job

# 1. Create/Get Employer
email = 'ANKURRAJ2005RAJ@gmail.com'
password = 'Raj@1234'

user, created = User.objects.get_or_create(
    email=email,
    defaults={
        'first_name': 'LPU',
        'last_name': 'Employer',
        'role': 'employer',
        'gender': 'M',
        'is_active': True,
    }
)

if created:
    user.set_password(password)
    user.save()
    print(f'Created employer account: {email}')
else:
    # Ensure role is employer and set/reset password to Raj@1234
    user.role = 'employer'
    user.set_password(password)
    user.save()
    print(f'Verified and updated employer account: {email}')

# 2. Verify/Create Categories
categories_names = ['Software Development', 'Marketing', 'Design', 'Data Science', 'Sales']
categories = {}
for name in categories_names:
    cat, created_cat = Category.objects.get_or_create(name=name)
    categories[name] = cat
    if created_cat:
        print(f'Created category: {name}')

# 3. 9 Jobs to Seed
jobs_to_seed = [
    {
        'title': 'Software Developer',
        'category': 'Software Development',
        'salary': '$800 - $1200',
        'location': 'Phagwara',
        'job_type': '2',  # Part time
        'company_name': 'GOOGLE',
        'url': 'https://www.google.com',
        'description': '<p>We are looking for a Software Developer to work on search algorithms and backend systems in our Phagwara office.</p>',
    },
    {
        'title': 'Django Backend Engineer',
        'category': 'Software Development',
        'salary': '$1200 - $1800',
        'location': 'Remote',
        'job_type': '1',  # Full time
        'company_name': 'Django Corp',
        'url': 'https://djangoproject.com',
        'description': '<p>Join our backend team to build APIs and clean codebases using Python and Django.</p>',
    },
    {
        'title': 'Frontend Developer',
        'category': 'Software Development',
        'salary': '$900 - $1300',
        'location': 'Bangalore',
        'job_type': '1',  # Full time
        'company_name': 'Meta',
        'url': 'https://meta.com',
        'description': '<p>Build interactive frontend interfaces using React, HTML5, and vanilla CSS.</p>',
    },
    {
        'title': 'UI/UX Designer',
        'category': 'Design',
        'salary': '$800 - $1100',
        'location': 'Phagwara',
        'job_type': '3',  # Internship
        'company_name': 'LPU Labs',
        'url': 'https://www.lpu.in',
        'description': '<p>Design web layouts, wireframes, and prototypes for campus management applications.</p>',
    },
    {
        'title': 'Graphic Designer',
        'category': 'Design',
        'salary': '$600 - $900',
        'location': 'Remote',
        'job_type': '2',  # Part time
        'company_name': 'Canva Partner',
        'url': 'https://canva.com',
        'description': '<p>Create visual resources, banners, and advertising templates for social media channels.</p>',
    },
    {
        'title': 'Digital Marketing Specialist',
        'category': 'Marketing',
        'salary': '$700 - $1000',
        'location': 'Phagwara',
        'job_type': '1',  # Full time
        'company_name': 'LPU Ventures',
        'url': 'https://www.lpu.in',
        'description': '<p>Manage social media accounts, SEO, and paid search campaigns to increase campus outreach.</p>',
    },
    {
        'title': 'Sales Representative',
        'category': 'Sales',
        'salary': '$500 - $800',
        'location': 'Delhi',
        'job_type': '1',  # Full time
        'company_name': 'Zomato',
        'url': 'https://zomato.com',
        'description': '<p>Onboard new restaurants, build relationships, and drive sales across the Delhi-NCR region.</p>',
    },
    {
        'title': 'Data Analyst',
        'category': 'Data Science',
        'salary': '$1000 - $1400',
        'location': 'Bangalore',
        'job_type': '1',  # Full time
        'company_name': 'Flipkart',
        'url': 'https://flipkart.com',
        'description': '<p>Work with large-scale datasets to build metrics and visual charts of consumer behavior.</p>',
    },
    {
        'title': 'Machine Learning Engineer',
        'category': 'Data Science',
        'salary': '$1500 - $2200',
        'location': 'Remote',
        'job_type': '1',  # Full time
        'company_name': 'OpenAI Partner',
        'url': 'https://openai.com',
        'description': '<p>Train, fine-tune, and deploy large language models and neural networks in production.</p>',
    },
]

total_seeded = 0
for index, job_data in enumerate(jobs_to_seed):
    # Ensure uniqueness using title and company name
    job, created_job = Job.objects.get_or_create(
        title=job_data['title'],
        company_name=job_data['company_name'],
        user=user,
        defaults={
            'description': job_data['description'],
            'salary': job_data['salary'],
            'location': job_data['location'],
            'job_type': job_data['job_type'],
            'category': categories[job_data['category']],
            'url': job_data['url'],
            'last_date': date.today() + timedelta(days=30 + index),
            'is_published': True,
            'is_closed': False,
        }
    )
    if created_job:
        total_seeded += 1
        print(f"[{total_seeded}] Seeded job: {job.title} under Category: {job_data['category']}")
    else:
        # If already exists, make sure it is assigned to this user and published
        job.user = user
        job.is_published = True
        job.is_closed = False
        job.save()
        print(f"Job already exists (verified): {job.title}")

print(f"\nDone! Successfully seeded/verified jobs. Total new jobs added: {total_seeded}")
