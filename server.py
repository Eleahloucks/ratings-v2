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

@app.route("/movies/<movie_id>/rating")
def movie_rating_page(movie_id):
    """Rate the selected movie."""
    movie = crud.get_movie_by_id(movie_id)
    return render_template("rating.html", movie = movie)
# Replace this with routes and view functions!

@app.route("/movies/<movie_id>/rating", methods=['POST'])
def add_rating(movie_id):
    rating = int(request.form.get('ratings-form'))
    user_session = crud.get_user_by_id(session['user_id'])
    movie_session = crud.get_movie_by_id(movie_id)

    rating_session = crud.create_rating(user_session, movie_session, rating)
    db.session.add(rating_session)
    db.session.commit()
    flash("Thanks for rating!")
    
    return redirect("/")



@app.route("/users")
def show_users():
    all_users = crud.get_all_users()
    return render_template("all_users.html", users = all_users)

@app.route("/users", methods=['POST'])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email):
        flash("Account already exists")
    else:
        new_user = crud.create_user(email, password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account was made")
    
    return redirect("/")

@app.route("/login", methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    potential_user = crud.get_user_by_email(email)
    if potential_user.password == password:
        session['user_id'] = potential_user.user_id
        flash('Logged in!')
    else:
        flash('Not logged in!')
    return redirect("/")

@app.route("/users/<user_id>")
def user_details(user_id):
    """Show details of a single user."""
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user = user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
