from rest_framework import serializers
from ..models import Job, Category, Applicant, BookmarkJob


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    # Nested read-only representation of category
    category = CategorySerializer(read_only=True)
    # Write-only field to accept category id on create/update
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('user', 'timestamp')


class ApplicantSerializer(serializers.ModelSerializer):
    # For reads: show nested job info
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_company = serializers.CharField(source='job.company_name', read_only=True)

    class Meta:
        model = Applicant
        fields = ('id', 'job', 'job_title', 'job_company', 'user', 'timestamp')
        read_only_fields = ('user', 'timestamp')


class BookmarkSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_company = serializers.CharField(source='job.company_name', read_only=True)
    job_location = serializers.CharField(source='job.location', read_only=True)

    class Meta:
        model = BookmarkJob
        fields = ('id', 'job', 'job_title', 'job_company', 'job_location', 'user', 'timestamp')
        read_only_fields = ('user', 'timestamp')
