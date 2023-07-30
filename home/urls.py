from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('all_movies/', views.all_movies, name='all_movies'),
    path('all_tv_shows/', views.all_tv_shows, name='all_tv_shows'),
    path('movie_details/<str:movie_id>/', views.movie_details, name='movie_details'),
    path('tv_show_details/<str:tv_show_id>/', views.tv_show_details, name='tv_show_details'),
    path('search/', views.search_results, name='search_results'),
    path('trending/', views.trending_movies, name='trending_movies'),
    path('about_us/', views.about_us, name='about_us'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),
    
]
