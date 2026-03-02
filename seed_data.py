import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')
django.setup()

from account.models import User
from jobapp.models import Category, Job
from datetime import date, timedelta

def seed_data():
    # 1. Create an Employer (Recruiter)
    employer_email = 'recruiter@example.com'
    if not User.objects.filter(email=employer_email).exists():
        employer = User.objects.create_user(
            email=employer_email,
            password='password123',
            first_name='John',
            last_name='Recruiter',
            role='employer',
            gender='M'
        )
        print(f"Created employer: {employer_email}")
    else:
        employer = User.objects.get(email=employer_email)

    # 2. Create Categories
    categories_names = ['Software Development', 'Marketing', 'Design', 'Data Science', 'Sales']
    categories = {}
    for name in categories_names:
        cat, created = Category.objects.get_or_create(name=name)
        categories[name] = cat
        if created:
            print(f"Created category: {name}")

    # 3. Create Sample Jobs
    sample_jobs = [
        {
            'title': 'Senior Python Developer',
            'category': 'Software Development',
            'company': 'Tech Solutions',
            'location': 'New York, NY',
            'type': '1', # Full-time
            'salary': '$120k - $150k'
        },
        {
            'title': 'Digital Marketing Specialist',
            'category': 'Marketing',
            'company': 'Growth Ads',
            'location': 'Remote',
            'type': '2', # Part-time
            'salary': '$40/hour'
        },
        {
            'title': 'UI/UX Designer',
            'category': 'Design',
            'company': 'Creative Studio',
            'location': 'San Francisco, CA',
            'type': '1', # Full-time
            'salary': '$110k - $130k'
        },
        {
            'title': 'Data Analyst Intern',
            'category': 'Data Science',
            'company': 'Data Insights',
            'location': 'Chicago, IL',
            'type': '3', # Internship
            'salary': '$30/hour'
        },
        {
            'title': 'Account Executive',
            'category': 'Sales',
            'company': 'Global Sales Co',
            'location': 'Austin, TX',
            'type': '1', # Full-time
            'salary': '$80k + Commission'
        }
    ]

    for job_data in sample_jobs:
        if not Job.objects.filter(title=job_data['title'], company_name=job_data['company']).exists():
            job = Job.objects.create(
                user=employer,
                title=job_data['title'],
                description=f"<p>We are looking for a skilled {job_data['title']} to join our team at {job_data['company']}.</p>",
                location=job_data['location'],
                job_type=job_data['type'],
                category=categories[job_data['category']],
                salary=job_data['salary'],
                company_name=job_data['company'],
                url='https://example.com',
                last_date=date.today() + timedelta(days=30),
                is_published=True
            )
            print(f"Created job: {job.title}")

if __name__ == '__main__':
    seed_data()
