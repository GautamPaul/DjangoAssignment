from functools import partial
import re
from django.shortcuts import render
from projects.models import Projects, Release, Resource
from projects.serializers import ProjectsSerializer, ReleaseSerializer, ResourceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import Http404
from rest_framework import status
import json
import io
from rest_framework.parsers import JSONParser


# Create your views here.

def home(request):
    return render(request, 'index.html')


class AllResources(APIView):
    # method to get all the Resources
    def get(self, request):
        resources = Resource.objects.all()
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

    # method to create a Resource
    def post(self, request):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SpecificResource(APIView):
    def get_resource(self, pk):
        try:
            return Resource.objects.get(pk=pk)
        except:
            raise Http404

    # method to handle the get request for a specific resource (Request)
    def get(self, request, pk):
        resource = self.get_resource(pk)
        serializer = ResourceSerializer(resource)
        return Response(serializer.data)

    # method to handle the put request to update specific resource (Update)
    def put(self, request, pk):
        resource = self.get_resource(pk)
        serializer = ResourceSerializer(
            resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # method to handle the delete request (Delete)
    def delete(self, request, pk):
        resource = self.get_resource(pk)
        resource.delete()
        return Response({'response': 'resource deleted'}, status=status.HTTP_204_NO_CONTENT)


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
        serializer = ProjectsSerializer(
            project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # method to handle the delete request (Delete)
    def delete(self, request, pk):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllocateResource(APIView):
    # method to allocate single/multiple resources
    def put(self, request, pk):
        # converting json object to python dict and then extracting the resources as a list
        resources = json.loads(request.body)["id"]

        # checking the existence of project
        project = Projects.objects.get(id=pk)
        if project.exists():
            # iterating through the resources
            for resource in resources:
                # checking the existence of user
                resource = Resource.objects.filter(id=resource)
                if resource.exists():
                    # getting the current data of the resource

                    resourceData = Resource.objects.get(id=resource)
                    # updating the project of the resource
                    serializer = ResourceSerializer(
                        resourceData, data={"project": pk}, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                else:
                    return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class DeallocateResource(APIView):
    # method to deallocate single/multiple resources
    def put(self, request):
        resources = json.loads(request.body)["id"]
        print(resources)
        for resource in resources:
            currentResource = Resource.objects.get(id=resource)
            if currentResource.exists():
                # getting the current data of the resource
                resourceData = Resource.objects.get(id=resource)

                # updating the project of the resource and setting it back to the common project
                serializer = ResourceSerializer(
                    resourceData, data={"project": 1}, partial=True)
                if serializer.is_valid():
                    serializer.save()
            else:
                return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class CreateRelease(APIView):
    def post(self, request, pk):
        # modifying the project attribute in the data with the target project
        # request.data["project"] = pk
        project = Projects.objects.filter(id=pk)
        if project.exists():
            serializer = ReleaseSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ListReleases(APIView):
    # method to list all the releases of a project
    def get(self, request, pk):
        releases = Release.objects.filter(project_id=pk)
        serializer = ReleaseSerializer(releases, many=True)
        return Response(serializer.data)
