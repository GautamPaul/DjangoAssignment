from django.urls import path
from projects import views

urlpatterns = [
    path('', views.home),
    path('projects/', views.AllProjects.as_view()),
    path('projects/<int:pk>/', views.SpecificProject.as_view()),

]
