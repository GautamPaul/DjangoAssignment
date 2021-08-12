from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import Projects


# Project Serializer
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'
