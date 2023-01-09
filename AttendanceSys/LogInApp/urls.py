from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('logIn', views.logInPage, name='logIn'),
    path('mainPage', views.mainPage, name='mainPage'),
    path('logOut', views.logOutPage, name='logOut'),
    path('viewCourse', views.viewCourse, name='viewCourse'),
    path('cameraCap', views.cameraCap, name='cameraCap'),
    path('viewStudents', views.viewStudents, name='viewStudents'),
    path('registerStudents', views.registerStudents, name='registerStudents'),
    path('viewAttendance', views.viewAttendance, name='viewAttendance'),
    path('saveAttendance', views.saveAttendance, name='saveAttendance'),
    path('viewReport', views.viewReport, name='viewReport'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('contactUs', views.contactUs, name='contactUs'),

]

