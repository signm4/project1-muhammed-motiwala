import flask
import requests
from dotenv import load_dotenv


def main():

    movieList =["Tron", "Fast and Furious", "IronMan"]
    enumerate_object = enumerate(movieList) # the enumerate object
    iteration = next(enumerate_object) # first iteration from enumerate
    #print(iteration)

    class Movie:
        def __init__(self, title, key):
            self.title = title
            self.key = key

    m1 = Movie("Tron", 20526)
    m2 = Movie("Fast & Furious", 13804)
    m3 = Movie("Iron Man", 1726)

    #see if dictionary is working
    # print(m1.title)
    # print(m1.key)



    print("here are my favorite movies: ")
    for index, item in enumerate(movieList, start=0):   # Python indexes start at zero
        print((index + 1), item)

    #int(chosenMovie)

    choice = input("choose one of my favorite movies: ")
    choice = int(choice)
    print(choice)
     
    if choice == 1:
        movieIndex = m1
        chosenMovie = movieList[0]
    elif choice == 2:
        movieIndex = m2
        chosenMovie = movieList[1]
    elif choice == 3:
        movieIndex = m3
        chosenMovie = movieList[2]
    else:
        print("invalid choice restart program")
        quit()



    choice = choice - 1 #contains our index 
    print("the chosen movie is: " + chosenMovie)

#USING API
    #using dot env file and pulling key from .env file
    load_dotenv()
    api_key = os.getenv('TMDB_API_KEY')

    #made base URL, requests.get will pull the movie details, also need api key to access
    TMDB_MOVIE_API_REQUEST = 'https://api.themoviedb.org/3'
    movie_id = "movieIndex.key" # need to figure out how to call dictionary
    response =  requests.get(
        f"{TMDB_MOVIE_API_REQUEST}/movie/{movie_id}",
        params={'api_key' : api_key }
        )

main()