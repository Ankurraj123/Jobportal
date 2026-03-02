from django.urls import path
from .views import (
    JobListAPIView,
    JobDetailAPIView,
    JobCreateAPIView,
    JobUpdateAPIView,
    JobDeleteAPIView,
    CategoryListAPIView,
    ApplicantAPIView,
    BookmarkAPIView,
    BookmarkDeleteAPIView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListAPIView.as_view(), name='api-category-list'),

    # Jobs
    path('jobs/', JobListAPIView.as_view(), name='api-job-list'),
    path('jobs/create/', JobCreateAPIView.as_view(), name='api-job-create'),
    path('jobs/<int:id>/', JobDetailAPIView.as_view(), name='api-job-detail'),
    path('jobs/<int:id>/update/', JobUpdateAPIView.as_view(), name='api-job-update'),
    path('jobs/<int:id>/delete/', JobDeleteAPIView.as_view(), name='api-job-delete'),

    # Applicants (apply for a job / view applications)
    path('applicants/', ApplicantAPIView.as_view(), name='api-applicant-list'),

    # Bookmarks (save a job / view saved jobs)
    path('bookmarks/', BookmarkAPIView.as_view(), name='api-bookmark-list'),
    path('bookmarks/<int:pk>/', BookmarkDeleteAPIView.as_view(), name='api-bookmark-delete'),
]
