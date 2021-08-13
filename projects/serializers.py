from django.db.models import fields
from django.db.models.base import Model
from rest_framework import serializers
from .models import Projects, Resource, Release


# Project Serializer
class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'


# Resource Serializer
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


# Release Serializer
class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = '__all__'
