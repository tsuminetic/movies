import os
import json
import random
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
import pymongo

# Set up the MongoDB connection
client = pymongo.MongoClient('localhost', 27017)  
db = client['movie_database'] 
collection = db['movies'] 

dbtv = client['tv_show_database']  # Replace 'tv_show_database' with your desired database name
collectiontv = dbtv['tv_shows'] 

def import_movies_to_mongodb():
    with open('data/movie_data.json') as json_file:
        movies_data = json.load(json_file)

    collection.insert_many(movies_data)
def import_tv_shows_to_mongodb():
    with open('data/tv_show_data.json') as json_file:
        tv_shows_data = json.load(json_file)

    # Insert the TV show data into the MongoDB collection
    collectiontv.insert_many(tv_shows_data)


def movie_details(request, movie_id):
    # Fetch the movie data from the MongoDB collection
    movie = collection.find_one({'movie_id': movie_id})

    if movie is None:
        return render(request, 'movie_not_found.html')

    min_common_genres = 2

    # Find similar movies based on common genres
    similar_movies = [other_movie for other_movie in collection.find({
        'genres': {'$in': movie['genres']},
        'movie_id': {'$ne': movie_id}
    }) if len(set(other_movie['genres']) & set(movie['genres'])) >= min_common_genres]

    random.shuffle(similar_movies)

    num_similar_movies_to_display = 10
    similar_movies = similar_movies[:num_similar_movies_to_display]

    context = {
        'movie': movie,
        'similar_movies': similar_movies,
    }

    return render(request, 'components/movie_details.html', context)

def tv_show_details(request, tv_show_id):
    # Fetch the TV show data from the MongoDB collection
    tv_show = collectiontv.find_one({'tv_show_id': tv_show_id})

    if tv_show is None:
        return render(request, 'tv_show_not_found.html')

    min_common_genres = 2

    # Find similar TV shows based on common genres
    similar_tv_shows = [other_tv_show for other_tv_show in collectiontv.find({
        'genres': {'$in': tv_show['genres']},
        'tv_show_id': {'$ne': tv_show_id}
    }) if len(set(other_tv_show['genres']) & set(tv_show['genres'])) >= min_common_genres]

    random.shuffle(similar_tv_shows)

    num_similar_tv_shows_to_display = 10
    similar_tv_shows = similar_tv_shows[:num_similar_tv_shows_to_display]

    context = {
        'tv_show': tv_show,
        'similar_tv_shows': similar_tv_shows,
    }

    return render(request, 'components/tv_show_details.html', context)

def all_movies(request):
    # Fetch all movies from the MongoDB collection
    movies_data = list(collection.find({}))

    paginator = Paginator(movies_data, 35)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'active_tab': 'movies',
        'page_obj': page_obj,
    }
    return render(request, 'components/all_movies.html', context)

def all_tv_shows(request):
    # Fetch all TV shows from the MongoDB collection
    tv_shows_data = list(collectiontv.find({}))

    paginator = Paginator(tv_shows_data, 35)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'active_tab': 'tv_shows',
        'page_obj': page_obj,
    }
    return render(request, 'components/all_tv_shows.html', context)


def search_results(request):
    query = request.GET.get('q')
    if query:
        movie_data = collection.find()
        tv_show_data = collectiontv.find()

        search_terms = query.lower().split()

        def get_relevance(item):
            movie_name = item.get('movie_name', '').lower()
            tv_show_name = item.get('tv_show_name', '').lower()

            return all(term in movie_name or term in tv_show_name for term in search_terms)

        movie_results = [item for item in movie_data if get_relevance(item)]
        tv_show_results = [item for item in tv_show_data if get_relevance(item)]

        results = movie_results + tv_show_results

    else:
        results = []

    results = sorted(results, key=lambda item: sum(term in item.get('movie_name', '').lower() + item.get('tv_show_name', '').lower() for term in search_terms), reverse=True)

    context = {
        'results': results,
        'query': query,
    }
    return render(request, 'components/search_results.html', context)



def trending_movies(request):
    
    with open('data/trending.json', 'r') as file:
        movies_data = json.load(file)

    
    trending_movies = movies_data[:16]

    
    return render(request, 'components/trending_movies.html', {'trending_movies': trending_movies})

def about_us(request):
    context = {
        'active_tab': 'about_us',
    }
    return render(request, 'components/about_us.html',context)

def terms(request):
    return render(request, 'components/terms.html')

def contact(request):
    return render(request, 'components/contact.html')

def home(request):
    
    with open('data/trending.json') as json_file:
        movies_data = json.load(json_file)

    
    top_50_movies = movies_data[:250]

    
    random_featured_movies = random.sample(top_50_movies, 3)

    
    trending_movies = [movie for movie in top_50_movies if movie not in random_featured_movies]

    random_trending_movies = random.sample(trending_movies, 4)

    context = {
        'active_tab': 'home',
        'random_movies': random_featured_movies,
        'random_trending_movies': random_trending_movies,
    }
    return render(request, 'components/index.html', context)