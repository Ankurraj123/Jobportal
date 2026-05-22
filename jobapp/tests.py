from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from jobapp.models import Category, Job
import datetime

User = get_user_model()

class JobAppTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            role="employer",
            gender="M"
        )
        # Create category
        self.category = Category.objects.create(name="Software Engineering")
        
        # Create a job
        self.job = Job.objects.create(
            user=self.user,
            title="Django Developer",
            description="Looking for a Python/Django developer.",
            location="Remote",
            job_type="1",  # Full time
            category=self.category,
            salary="100,000",
            company_name="Acme Corp",
            url="https://example.com",
            last_date=datetime.date.today() + datetime.timedelta(days=30),
            is_published=True,
            is_closed=False
        )
        self.job.tags.add("python", "django")
        
        self.client = Client()

    def test_category_creation(self):
        """Test Category model str method and creation."""
        self.assertEqual(str(self.category), "Software Engineering")

    def test_job_creation(self):
        """Test Job model str method and creation."""
        self.assertEqual(str(self.job), "Django Developer")
        self.assertEqual(self.job.location, "Remote")
        self.assertEqual(self.job.job_type, "1")

    def test_home_view(self):
        """Test the home page rendering."""
        response = self.client.get(reverse("jobapp:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobapp/index.html")

    def test_job_list_view(self):
        """Test the job list page rendering."""
        response = self.client.get(reverse("jobapp:job-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobapp/job-list.html")

    def test_single_job_view(self):
        """Test rendering of a single job details page."""
        response = self.client.get(reverse("jobapp:single-job", kwargs={"id": self.job.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobapp/job-single.html")

    def test_search_result_view(self):
        """Test searching for jobs."""
        response = self.client.get(reverse("jobapp:search_result"), {"job_title_or_company_name": "Django"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "jobapp/result.html")
        self.assertContains(response, "Django Developer")
