"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    """Show homepage"""

    return render_template("homepage.html")

@app.route("/movies")
def show_all_movies():
    """Show all movies"""
    all_movies = crud.get_all_movies()
    return render_template("all_movies.html", movies = all_movies)

@app.route("/movies/<movie_id>")
def movie_details(movie_id):
    """Show details of a single movie."""
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie = movie)
# Replace this with routes and view functions!

@app.route("/users")
def show_users():
    all_users = crud.get_all_users()
    return render_template("all_users.html", users = all_users)

@app.route("/users/<user_id>")
def user_details(user_id):
    """Show details of a single user."""
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user = user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
