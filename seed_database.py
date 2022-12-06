"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

##seed db hosts sample data in db

#getting rid of db in case its filled with junk
os.system("dropdb ratings")
#creating a db in psql so we have something to connect to and store data
os.system('createdb ratings')
#connecting to db
model.connect_to_db(server.app)
#tells sqlalchemy to create all the tables
model.db.create_all()


#load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    release_date_as_str = movie['release_date']

    #formate datetimeobject
    format = "%Y-%m-%d"
    release_date_as_datet = datetime.strptime(release_date_as_str, format)

    #creates movie from function in crud
    movie_object = crud.create_movie(title, overview, release_date_as_datet, poster_path)
    movies_in_db.append(movie_object)

#add movies to sql session and commit
model.db.session.add_all(movies_in_db)
model.db.session.commit()


#empty user list and rating list
user_list = []
rating_list = []

#generating 10 users with emails and rating
for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    #create a user here
    new_user = crud.create_user(email=email, password=password)
    user_list.append(new_user)

    #create 10 ratings for the user
    for i in range(10):
      #generate random score
      score = randint(1,5)
      #generate random movie
      movie = choice(movies_in_db)
      #new rating uses the crud function below and pull the move and score from above
      new_rating = crud.create_rating(user = new_user, movie = movie, score = score)
      #add the new rating to list
      rating_list.append(new_rating)

    #add user list and rating list to session and commit
    model.db.session.add_all(user_list)
    model.db.session.add_all(rating_list)
    model.db.session.commit()

