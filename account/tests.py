from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAccountTests(TestCase):
    def test_create_employee_user(self):
        """Test creating a regular user with employee role."""
        email = "employee@example.com"
        password = "password123"
        user = User.objects.create_user(
            email=email,
            password=password,
            role="employee",
            gender="M",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.role, "employee")
        self.assertEqual(user.gender, "M")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.get_full_name(), "John Doe")
        self.assertEqual(str(user), email)

    def test_create_employer_user(self):
        """Test creating a user with employer role."""
        email = "employer@example.com"
        password = "password123"
        user = User.objects.create_user(
            email=email,
            password=password,
            role="employer",
            gender="F",
            first_name="Jane",
            last_name="Smith"
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.role, "employer")
        self.assertEqual(user.gender, "F")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.get_full_name(), "Jane Smith")

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = "admin@example.com"
        password = "adminpassword"
        admin_user = User.objects.create_superuser(
            email=email,
            password=password
        )
        self.assertEqual(admin_user.email, email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
