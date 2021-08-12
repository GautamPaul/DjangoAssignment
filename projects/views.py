import re
from django.shortcuts import render
from projects.models import Projects
from projects.serializers import ProjectsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import Http404
from rest_framework import status


# Create your views here.

def home(request):
    return render(request, 'index.html')


class AllProjects(APIView):
    # method to get all the projects available (Request)
    def get(self, request):
        projects = Projects.objects.all()
        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data)

    # method to handle the post request to create new project (Create)
    def post(self, request):
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecificProject(APIView):
    def get_project(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except:
            raise Http404

    # method to handle the get request for a specific project (Request)
    def get(self, request, pk):
        project = self.get_project(pk)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

    # method to handle the put request to update specific project (Update)
    def put(self, request, pk):
        project = self.get_project(pk)
        serializer = ProjectsSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # method to handle the delete request (Delete)
    def delete(self, request, pk):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
