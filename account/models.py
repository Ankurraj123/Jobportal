from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import CustomUserManager

GENDER_TYPE = (
    ('M', "Male"),
    ('F', "Female"),

)

ROLE = (
    ('employer', "Employer"),
    ('employee', "Employee"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    role = models.CharField(choices=ROLE,  max_length=10)
    gender = models.CharField(choices=GENDER_TYPE, max_length=1)
    
    # New fields for CV and Profile
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)  # comma-separated
    education = models.TextField(null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    # Parsed CV structured sections
    cv_projects = models.JSONField(null=True, blank=True, default=list)
    cv_certificates = models.JSONField(null=True, blank=True, default=list)
    cv_training = models.JSONField(null=True, blank=True, default=list)
    cv_achievements = models.JSONField(null=True, blank=True, default=list)
    cv_links = models.JSONField(null=True, blank=True, default=dict)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name+ ' ' + self.last_name
    objects = CustomUserManager()
