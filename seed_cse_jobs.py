"""
Seed script: add "B.Tech CSE" category and seed 10 CSE job positions under ANKURRAJ2005RAJ@gmail.com.
Run: python seed_cse_jobs.py
"""
import os
import django
from datetime import date, timedelta

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job.settings')

# Use Atlas MongoDB production URI by default if MONGODB_URI is not set in environment
if not os.environ.get('MONGODB_URI'):
    os.environ['MONGODB_URI'] = "mongodb+srv://ankur123:ankur%40123@cluster0.lswjemc.mongodb.net/jobportal_db?retryWrites=true&w=majority&appName=Cluster0"

django.setup()

from account.models import User
from jobapp.models import Category, Job

# 1. Get or Create the Employer
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
    # Ensure role is employer and password is correct
    user.role = 'employer'
    user.set_password(password)
    user.save()
    print(f'Verified employer account: {email}')

# 2. Get or Create Category: "B.Tech CSE"
category_name = "B.Tech CSE"
category, created_cat = Category.objects.get_or_create(name=category_name)
if created_cat:
    print(f'Created Category: {category_name}')
else:
    print(f'Verified Category: {category_name}')

# 3. Define 10 job positions for B.Tech CSE students
cse_jobs = [
    {
        'title': 'Software Development Engineer (SDE) Intern',
        'salary': '₹25,000 - ₹35,000 / month',
        'location': 'Phagwara',
        'job_type': '3',  # Internship
        'company_name': 'Google',
        'url': 'https://www.google.com',
        'description': '<p>We are seeking a Software Development Engineer Intern who is currently pursuing a B.Tech in Computer Science & Engineering. You will work on building scalable APIs, optimizing web performance, and writing clean, testable code in Python and Go.</p>',
    },
    {
        'title': 'Frontend Developer (React)',
        'salary': '₹6 - ₹10 LPA',
        'location': 'Bangalore',
        'job_type': '1',  # Full time
        'company_name': 'Microsoft',
        'url': 'https://microsoft.com',
        'description': '<p>Looking for a Frontend Developer with strong knowledge of HTML, CSS, JavaScript, and React. Excellent UI/UX design sensibilities are a plus. Candidates should have a B.Tech CSE degree.</p>',
    },
    {
        'title': 'Backend Developer (Django & PostgreSQL)',
        'salary': '₹8 - ₹12 LPA',
        'location': 'Remote',
        'job_type': '1',  # Full time
        'company_name': 'Django Solutions',
        'url': 'https://djangoproject.com',
        'description': '<p>Build robust API services and integrate database systems. Experience with Python, Django, and PostgreSQL is required. Suitable for B.Tech CSE graduates.</p>',
    },
    {
        'title': 'Data Analyst Intern',
        'salary': '₹20,000 / month',
        'location': 'Phagwara',
        'job_type': '3',  # Internship
        'company_name': 'LPU Ventures',
        'url': 'https://www.lpu.in',
        'description': '<p>Help gather, clean, and visualize data using Python, Pandas, and Tableau. Ideal for B.Tech CSE students interested in data science.</p>',
    },
    {
        'title': 'Machine Learning Engineer Intern',
        'salary': '₹30,000 / month',
        'location': 'Remote',
        'job_type': '3',  # Internship
        'company_name': 'OpenAI Partner',
        'url': 'https://openai.com',
        'description': '<p>Work on fine-tuning neural networks and evaluating model outputs. Strong mathematics and Python skills are required. B.Tech CSE students preferred.</p>',
    },
    {
        'title': 'Cloud Support Associate',
        'salary': '₹5 - ₹8 LPA',
        'location': 'Hyderabad',
        'job_type': '1',  # Full time
        'company_name': 'Amazon Web Services',
        'url': 'https://aws.amazon.com',
        'description': '<p>Assist clients with cloud architecture deployment and troubleshooting on AWS. Perfect entry-level role for B.Tech CSE graduates.</p>',
    },
    {
        'title': 'Cybersecurity Analyst Intern',
        'salary': '₹22,000 / month',
        'location': 'Delhi NCR',
        'job_type': '3',  # Internship
        'company_name': 'QuickHeal Technologies',
        'url': 'https://www.quickheal.co.in',
        'description': '<p>Assist in monitoring networks for security breaches and conducting vulnerability scans. Ideal for B.Tech CSE students specializing in cybersecurity.</p>',
    },
    {
        'title': 'DevOps Engineer (Junior)',
        'salary': '₹7 - ₹10 LPA',
        'location': 'Pune',
        'job_type': '1',  # Full time
        'company_name': 'RedHat',
        'url': 'https://redhat.com',
        'description': '<p>Work on CI/CD pipelines, Docker containerization, and Kubernetes orchestration. Suitable for B.Tech CSE freshers.</p>',
    },
    {
        'title': 'Android App Developer Intern',
        'salary': '₹15,000 - ₹20,000 / month',
        'location': 'Phagwara',
        'job_type': '3',  # Internship
        'company_name': 'LPU Mobile Apps',
        'url': 'https://www.lpu.in',
        'description': '<p>Develop and maintain mobile applications using Kotlin or Flutter. B.Tech CSE students with mobile dev projects are preferred.</p>',
    },
    {
        'title': 'QA Test Engineer',
        'salary': '₹15,000 / month',
        'location': 'Remote',
        'job_type': '2',  # Part time
        'company_name': 'BrowserStack',
        'url': 'https://www.browserstack.com',
        'description': '<p>Write automated test cases using Selenium or PyTest, and perform manual testing. Open to B.Tech CSE students.</p>',
    },
]

total_seeded = 0
for index, job_data in enumerate(cse_jobs):
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
            'category': category,
            'url': job_data['url'],
            'last_date': date.today() + timedelta(days=30 + index),
            'is_published': True,
            'is_closed': False,
        }
    )
    if created_job:
        total_seeded += 1
        print(f"[{total_seeded}] Seeded B.Tech CSE job: {job.title} at {job.company_name}")
    else:
        # Update existing to ensure correct category and parameters
        job.category = category
        job.user = user
        job.is_published = True
        job.is_closed = False
        job.save()
        print(f"B.Tech CSE job already exists (verified/updated): {job.title}")

print(f"\nDone! Successfully seeded/verified {total_seeded} new B.Tech CSE jobs under category 'B.Tech CSE'.")
