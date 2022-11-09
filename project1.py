'''importing flask server to help deploy'''
import flask
'''importing os to get env key from other file'''
import os
'''importing requests to use for API'''
import requests
'''import flask sql'''
from flask_sqlalchemy import SQLAlchemy

import random
from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)


'''Selects a random movie from list'''
def randomMovieGen():
    movieList =["Tron", "Fast and Furious", "IronMan", "Spider Man: No Way Home", "Free Guy", "Shang-Chi", "The Godfather"]
    movieList_key = [20526, 13804, 1726, 634649, 550988, 566525, 238]

    # print("here is a favorite movie: ")

    randomSelect = random.choice(movieList)
    #  print(randomSelect)
    index = movieList.index(randomSelect)
    return (movieList_key[index])


'''Pulls the movie data from the database and returns it'''
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

'''takes in the given movie data and is able to figure the link of the poster image and returns the whole url'''
def getPoster(chosenMovie):
    movie_data = chosenMovie
    posterPath =  (movie_data["poster_path"])
    imageUrl = "https://image.tmdb.org/t/p/w500"
    return (imageUrl + posterPath)

'''Takes in given movie data and is able to return the genre(s)'''
def getGenre(chosenMovie):
    movie_data = chosenMovie
    # print("\nthe Genres are: ")
    str1 = " "
    for i in movie_data["genres"]:
        str1 += (str(i["name"] + ", "))
    return str1

'''Takes in movie data and returns the original title'''
def getTitle(chosenMovie):
    movie_data = chosenMovie
    return((movie_data["original_title"]))

'''takes in movie data and returns the tagline'''
def getTagline(chosenMovie):
    movie_data = chosenMovie
    return((movie_data["tagline"]))

'''takes in the title from getTitle(), searches on Wiki Api for link and returns it'''
def pullWikiData(search1):
    WIKI_API_REQUEST = 'https://en.wikipedia.org/w/api.php?'
    response =  requests.get(
        f"{WIKI_API_REQUEST}",
        params={'action':'opensearch',
                 'namespace' : '0',
                 'search' : search1,
                 'limit' : '1',
                 'format' : 'json'}
        )

    json_data = response.json()

    wiki_data = json_data
    wiki_data_url = str(wiki_data[3][0])
    return ((wiki_data_url))

@app.route('/')
def main():
    chosenMovie = pullMovieData() # so it only generates the poster once
    # print ("\nThe title of the movie is: " + getTitle(chosenMovie))
    # print ("\nThe Genre is: " + getGenre(chosenMovie))
    # print("\nThe Tagline is: " + getTagline(chosenMovie))
    # print("\nHere is the poster: " + getPoster(chosenMovie))
    title1=getTitle(chosenMovie)

    return flask.render_template(
        'index.html',
    title=getTitle(chosenMovie),
    tagline=getTagline(chosenMovie),
    genres = getGenre(chosenMovie),
    poster = getPoster(chosenMovie),
    links = pullWikiData(title1)
        )

@app.route('/login')
def login():
    return flask.render_template('login.html')

@app.route('/handle_login', methods = ['POST'])
def handle_login():
    form_data = request.form
    global username; username = form_data['username']
    user = User.query.filter_by(username = username).first()
    login_user (user)
    return redirect(url_for('welcome'))


@app.route('/signup')
def signup():
    return flask.render_template('signup.html')

#getGenre(pullMovieData())

#main()
# app.run(debug=True)