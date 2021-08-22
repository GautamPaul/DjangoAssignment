from django.urls import path
from projects import views

urlpatterns = [
    path('', views.home),
    path('resources/', views.AllResources.as_view()),
    path('resources/<int:pk>/', views.SpecificResource.as_view()),
    path('projects/', views.AllProjects.as_view()),
    path('projects/<int:pk>/', views.SpecificProject.as_view()),
    path('allocateresource/<int:pk>/', views.AllocateResource.as_view()),
    path('deallocateresource/', views.DeallocateResource.as_view()),
    path('createrelease/<int:pk>/', views.CreateRelease.as_view()),
    path('listreleases/<int:pk>/', views.ListReleases.as_view())
]
