from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from ..utils import parse_resume
import os

User = get_user_model()

class RegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Check if resume is being uploaded
        resume_file = request.FILES.get('resume')
        self.perform_update(serializer)

        if resume_file:
            # Trigger parsing
            parsed_data = parse_resume(instance.resume.path)
            if parsed_data:
                instance.bio = parsed_data.get('bio')
                instance.skills = parsed_data.get('skills')
                instance.education = parsed_data.get('education')
                instance.experience = parsed_data.get('experience')
                instance.save()
                # Re-serialize to include parsed data in response
                serializer = self.get_serializer(instance)

        return Response(serializer.data)
