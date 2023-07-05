"""mydjangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
import mydjangoapp.view.myview as myview
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', lambda request:HttpResponse("Hey man, how are you")),
    path('welcome/', myview.welcome),
    path('add/', myview.add),
    path('mul/<int:a>/<int:b>', myview.mul),
    path('cao', myview.cao),
    path('palindrom/<str:rijec>', myview.palindrom),
    path('index', myview.index),
    path('about',myview.about),
    path('classes',myview.classes),
    path('instructors',myview.instructors),
    path('contact',myview.contact),
    path('blog',myview.blog),
    path('loggedinusers', myview.loggedin_users),
    path('api/register/', myview.register, name='register'),
    path('api/login/', myview.custom_login, name='login'),
    path('loggedinusers/', myview.loggedin_users, name='loggedin_users'), 
    path('api/newActor', myview.new_actor, name='newActor'),
    path('api/get_city_count/', myview.get_city_count, name='get_city_count'),
    path('api/movies/', myview.get_movies, name='get_movies'),  
    path('news/', myview.news_view, name='news'),
    path('movie/<int:movie_id>/', myview.movie_detail, name='movie_detail'),  # New URL pattern
]

