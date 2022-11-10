'''importing flask server to help deploy'''
import flask
from flask import Flask, flash, redirect, request, url_for, render_template 
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
'''importing os to get env key from other file'''
import os
'''importing requests to use for API'''
import requests
'''import flask sql'''
from flask_sqlalchemy import SQLAlchemy, session

import random
from dotenv import load_dotenv
load_dotenv()

app = flask.Flask(__name__)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)




@login_manager.user_loader
def load_user(id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Person.query.get(int(id))


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

def getID(chosenMovie):
    movie_data = chosenMovie
    return((movie_data["id"]))

'''takes in movie data and returns the tagline'''
def getTagline(chosenMovie):
    movie_data = chosenMovie
    return((movie_data["tagline"]))

def getReview(chosenMovie):
    db_data = Review.query.filter_by(movie_id=getID(chosenMovie)).all()
    print ("getReview function says: ", db_data)
    return(db_data)

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

class Person(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True, nullable = False)

    def __repr__(self):
        return '<Review %r>' % self.username

    def __repr__(self) -> str:
        return f"Person with username: {self.username}"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable = False)
    movie_id = db.Column(db.Integer, nullable = False)
    movie_review= db.Column(db.String(800), nullable = False)
    movie_rating = db.Column(db.Integer, nullable = False)


with app.app_context():
    db.create_all()

   
@app.route('/signup.html')
def signup():
    return flask.render_template('signup.html')

@app.route('/index.html')
def main():
    chosenMovie = pullMovieData() # so it only generates the poster once
    # print ("\nThe title of the movie is: " + getTitle(chosenMovie))
    # print ("\nThe Genre is: " + getGenre(chosenMovie))
    # print("\nThe Tagline is: " + getTagline(chosenMovie))
    # print("\nHere is the poster: " + getPoster(chosenMovie))
    title1=getTitle(chosenMovie)
    # movie_id = chosenMovie
    db_data = getReview(chosenMovie)
    print(db_data)
    return flask.render_template(
        'index.html',
    movie_id = getID(chosenMovie),
    title=getTitle(chosenMovie),
    tagline=getTagline(chosenMovie),
    genres = getGenre(chosenMovie),
    poster = getPoster(chosenMovie),
    links = pullWikiData(title1),

    user = curr_user,
    db_data = db_data
        )
    

@app.route('/')
def login():
    return flask.render_template('login.html')

@app.route('/handle_login', methods = ['POST'])
def handle_login():
    username = request.form.get('username')
    if username == " ":
        flash("Invalid, Please try again")
        return redirect(url_for('login'))
    person = Person.query.filter_by(username = username).first()
    global curr_user
    curr_user = username
    # Person.query.filter_by(username)
    if person:
        login_user(person)
        print("User Accepted")
        return redirect(url_for('main'))
    else:
        flash("Failed Identity, Try again")
        print("User Declined")
        return(redirect(url_for('login')))
        
    # return flask.redirect(url_for('welcome'))



@app.route('/handle_signup', methods = ['POST'])
def handle_signup():

    # 
    if request.method == "POST":
        # getting input with name = fname in HTML form
        username = request.form.get("username")
        auth_user = Person(username = username)
        db.session.add(auth_user)
        db.session.commit()
        # flash( "Your name is "+ username )
        return redirect(url_for('login'))
        # return render_template("index.html")
    # return flask.redirect(url_for('welcome'))

@app.route('/handle_review', methods = ['POST'])
def comment():
    form_data = request.form
    # username = db.Column(db.String(80), nullable = True)
    movie_review= form_data['movie_review']
    movie_id = form_data['movie_id']
    movie_rating= form_data['movie_rating']
    movie_rating = int (movie_rating)
    if movie_rating == " ":
        flash("Try again")
        print ("movie rating was empty")
        return flask.render_template('index.html')
    elif movie_rating > 5 or movie_rating < 0:
        flash("Incorrect input, Try Again")
        print( "not a valid rating ")
        return flask.render_template('index.html')

    movie_comment = Review(username= curr_user, movie_id = movie_id, movie_review = movie_review, movie_rating = movie_rating)
    db.session.add(movie_comment)
    db.session.commit()
    flash("Review Recieved and Posted")
    # print(movie_comment)
    print ("review recieved, database updated")
    # return flask.render_template('index.html')
    return redirect(url_for('main'))

#getGenre(pullMovieData())

#main()
app.run(port=4500, debug=True)