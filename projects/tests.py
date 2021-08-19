from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Projects, Resource, Release
from rest_framework import status


# Create your tests here.

class ProjectsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Projects.objects.create(
            name='test project', expectedEndDate='2022-09-01')
        self.project.save()

    def test_createProject(self):
        beforeCreateCount = Projects.objects.all().count()
        print(beforeCreateCount)
        response = self.client.post('/projects/', data={"name": "Test Project 1",
                                                        "expectedEndDate": "2022-06-19"})
        afterCreateCount = Projects.objects.all().count()
        print(afterCreateCount)
        self.assertEqual(beforeCreateCount+1, afterCreateCount)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieveProject(self):
        id = self.project.id
        response = self.client.get(f'/projects/{id}/')
        self.assertEqual(response.data['name'], self.project.name)
        self.assertEqual(
            response.data['expectedEndDate'], self.project.expectedEndDate)

    def test_updateProject(self):
        response = self.client.put(
            f'/projects/{self.project.id}/', data={"expectedEndDate": "2022-10-19"})
        self.assertEqual(response.data['expectedEndDate'], '2022-10-19')

    def test_deleteProject(self):
        beforeDeleteCount = Projects.objects.all().count()
        response = self.client.delete(f'/projects/{self.project.id}/')
        afterDeleteCount = Projects.objects.all().count()
        self.assertEqual(beforeDeleteCount-1, afterDeleteCount)


class ReleaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Projects.objects.create(
            id=1, name="Test Project", expectedEndDate="2022-09-02")
        self.project.save()

    def test_createRelease(self):
        response = self.client.post(f'/createrelease/{self.project.id}/', data={
            "project": self.project.id, "release_date": "2021-08-24", "deliverables": "api"})
        self.assertEqual(response.data['deliverables'], "api")
