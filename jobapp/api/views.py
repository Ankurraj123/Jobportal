from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Job, Category, Applicant, BookmarkJob
from .serializers import (
    JobSerializer,
    CategorySerializer,
    ApplicantSerializer,
    BookmarkSerializer,
)


# ─── Category ───────────────────────────────────────────────────────────────

class CategoryListAPIView(generics.ListAPIView):
    """
    GET /api/categories/
    Returns all job categories. Public access.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# ─── Jobs ────────────────────────────────────────────────────────────────────

class JobListAPIView(generics.ListAPIView):
    """
    GET /api/jobs/
    List published jobs. Supports filtering:
      ?keyword=  ?location=  ?category=  ?job_type=
    Public access.
    """
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Job.objects.filter(is_published=True, is_closed=False).order_by('-timestamp')
        keyword = self.request.query_params.get('keyword')
        location = self.request.query_params.get('location')
        category = self.request.query_params.get('category')
        job_type = self.request.query_params.get('job_type')

        if keyword:
            queryset = queryset.filter(title__icontains=keyword) | queryset.filter(
                company_name__icontains=keyword
            )
        if location:
            queryset = queryset.filter(location__icontains=location)
        if category:
            queryset = queryset.filter(category__id=category)
        if job_type:
            queryset = queryset.filter(job_type=job_type)

        return queryset.distinct()


class JobDetailAPIView(generics.RetrieveAPIView):
    """
    GET /api/jobs/<id>/
    Retrieve a single job. Public access.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]


class JobCreateAPIView(generics.CreateAPIView):
    """
    POST /api/jobs/create/
    Create a new job. Requires authentication (employer only recommended).
    """
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobUpdateAPIView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/jobs/<id>/update/
    Update a job. Only the owner can update.
    """
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)


class JobDeleteAPIView(generics.DestroyAPIView):
    """
    DELETE /api/jobs/<id>/delete/
    Delete a job. Only the owner can delete.
    """
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)


# ─── Applicants ──────────────────────────────────────────────────────────────

class ApplicantAPIView(generics.ListCreateAPIView):
    """
    GET  /api/applicants/  — List applicants (employee sees own, employer sees theirs)
    POST /api/applicants/  — Apply for a job  { "job": <job_id> }
    Requires authentication.
    """
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        job_id = self.request.query_params.get('job_id')

        if user.role == 'employer':
            qs = Applicant.objects.filter(job__user=user).select_related('job', 'user')
            if job_id:
                qs = qs.filter(job__id=job_id)
            return qs

        # employee sees their own applications
        return Applicant.objects.filter(user=user).select_related('job')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ─── Bookmarks ───────────────────────────────────────────────────────────────

class BookmarkAPIView(generics.ListCreateAPIView):
    """
    GET  /api/bookmarks/  — List saved jobs for the current employee
    POST /api/bookmarks/  — Bookmark a job  { "job": <job_id> }
    Requires authentication.
    """
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookmarkJob.objects.filter(user=self.request.user).select_related('job')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookmarkDeleteAPIView(generics.DestroyAPIView):
    """
    DELETE /api/bookmarks/<id>/
    Remove a saved job. Only the owner can delete.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BookmarkJob.objects.filter(user=self.request.user)
