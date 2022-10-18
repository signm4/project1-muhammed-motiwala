import flask
import os
import requests
import random
from dotenv import load_dotenv

def randomMovieGen():
    movieList =["Tron", "Fast and Furious", "IronMan"]
    movieList_key = [20526, 13804, 1726]

    # print("here is a favorite movie: ")

    randomSelect = random.choice(movieList)
    #  print(randomSelect)
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

def getPoster(chosenMovie):
    movie_data = chosenMovie
    return (movie_data["poster_path"])

def getGenre(chosenMovie):
    movie_data = chosenMovie
    # print("\nthe Genres are: ")
    
    for i in movie_data["genres"]:
        return (i["name"] + " ")


def getTitle(chosenMovie):
    movie_data = chosenMovie
    return((movie_data["original_title"]))

def getTagline(chosenMovie):
    movie_data = chosenMovie
    return((movie_data["tagline"]))



def main():
    chosenMovie = pullMovieData() # so it only generates the poster once
    print ("\nThe title of the movie is: " + getTitle(chosenMovie))
    print ("\nThe Genre is: " + getGenre(chosenMovie))
    print("\nThe Tagline is: " + getTagline(chosenMovie))
    print("\nHere is the poster: " + getPoster(chosenMovie))

#getGenre(pullMovieData())

main()