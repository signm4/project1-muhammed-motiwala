import flask
import os
import requests
import random
from dotenv import load_dotenv

def randomMovieGen():
    movieList =["Tron", "Fast and Furious", "IronMan"]
    movieList_key = [20526, 13804, 1726]

    print("here is a favorite movie: ")

    randomSelect = random.choice(movieList)
    print(randomSelect)
    index = movieList.index(randomSelect)
    return (movieList_key[index])

def pullMovieData():
    #USING API
    #using dot env file and pulling key from .env file
    load_dotenv()
    api_key = os.getenv('TMDB_API_KEY')

    #made base URL, requests.get will pull the movie details, also need api key to access
    TMDB_MOVIE_API_REQUEST = 'https://api.themoviedb.org/3'
    rand_movie_id = randomMovieGen() # calls generator, generator returns movie_id
    movie_id = str(rand_movie_id)
    response =  requests.get(
        f"{TMDB_MOVIE_API_REQUEST}/movie/{movie_id}",
        params={'api_key' : api_key }
        )

    json_data = response.json()
    return json_data


def getGenre():
    
    movie_data = pullMovieData()

    print("\nthe Genres are: ")
    for i in movie_data["genres"]:
        print (i["name"])

def getTitle():

    movie_data = pullMovieData()
    print("\nThe offical title is : " + (movie_data["original_title"]))

def getTagline():
    movie_data = pullMovieData()
    print("the movie tagline is: " + (movie_data["tagline"]))



#def main():

# #USING API
#     #using dot env file and pulling key from .env file
#     load_dotenv()
#     api_key = os.getenv('TMDB_API_KEY')

#     #made base URL, requests.get will pull the movie details, also need api key to access
#     TMDB_MOVIE_API_REQUEST = 'https://api.themoviedb.org/3'
#     rand_movie_id = randomMovieGen() # calls generator, generator returns movie_id
#     movie_id = str(rand_movie_id)
#     response =  requests.get(
#         f"{TMDB_MOVIE_API_REQUEST}/movie/{movie_id}",
#         params={'api_key' : api_key }
#         )

getTagline()