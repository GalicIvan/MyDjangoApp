from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import models
import json
from django.shortcuts import get_object_or_404
from django.db import connection
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from xml.etree import ElementTree

def welcome(request):
    return HttpResponse("Hello and welcome!")

def add(request):
    a = int(request.GET.get("a"))
    b = int(request.GET.get("b"))
    return HttpResponse(f"Result is: {a+b}")

def mul(request,a,b):
    return HttpResponse(f"Result is: {a*b}")

def cao(request):
    username="almas"
    firstname = "Almas"
    lastname = "Delic"
    return render(request,"hello.html",locals())

def palindrom(request,rijec):
    novaRijec = rijec
    jelPalindrom = ""
    if (novaRijec == rijec[::-1]):
        jelPalindrom = "Palindrom"
    else:
        jelPalindrom = "Nije palindrom"
    return render(request,"palindrom.html",locals())
    
def index(request):
    return render(request,'index.html',locals())

def about(request):
    return render(request, 'about.html',locals())

def classes(request):
    return render(request,'classes.html',locals())

def instructors(request):
    return render(request,'instructors.html',locals())

def contact(request):
    return render(request,'contact.html',locals())

def blog(request):
    return render(request,'blog.html',locals())

@csrf_exempt
def new_actor(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO staff (first_name, last_name) VALUES (%s, %s)", [first_name, last_name])

        return JsonResponse({'message': 'Actor added successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=405) 

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists.'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({'message': 'Registration successful.'}, status=200)

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=401)

@login_required()
def loggedin_users(request):
    return render(request, 'loggedinusers.html')



class Movie(models.Model):
    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        db_table = 'Film'

def get_movies(request):
    movies = Movie.objects.all()[:10]  # Retrieve the first 10 movies
    movie_list = []
    for movie in movies:
        movie_data = {
            'id': movie.film_id,
            'title': movie.title,
            'description': movie.description,
        }
        movie_list.append(movie_data)

    return JsonResponse(movie_list, safe=False)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, film_id=movie_id)
    context = {
        'movie': movie
    }
    return render(request, 'movie_detail.html', context)


def get_city_count(request):
    country = request.GET.get('country')  
    query = """
        SELECT COUNT(*) as city_count
        FROM city c
        INNER JOIN country co ON c.country_id = co.country_id
        WHERE co.country = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [country])
        result = cursor.fetchone()
        city_count = result[0] if result else 0

    return JsonResponse({'city_count': city_count})

def news_view(request):
    url = 'https://news.yahoo.com/rss/'

    response = requests.get(url)

    if response.status_code == 200:
        news_data = parse_rss(response.content)
    else:
        news_data = []
    
    paginator = Paginator(news_data, 12) 
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
    }
    print(page_obj, "TESTIRAM")
    return render(request, 'blog.html', context)

def parse_rss(xml_content):

    root = ElementTree.fromstring(xml_content)
    news_data = []  
    for item in root.iter('item'):
        title = item.find('title').text
        image_url = get_image_url(item)

        news_item = {
            'title': title,
            'image_url': image_url
        }
        news_data.append(news_item)

    return news_data


def get_image_url(item):
    image_url = None
    # Provjeravamo da li media content element ima URL attribute
    media_content_element = item.find('.//{http://search.yahoo.com/mrss/}content')
    if media_content_element is not None and 'url' in media_content_element.attrib:
        image_url = media_content_element.attrib['url']

    return image_url
