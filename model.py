"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model): #one user has many bookings - one to many relationship
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    img = db.Column(db.String)

    location = db.relationship("Location", back_populates="user")
    review = db.relationship("Review", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email} fname={self.fname} lname ={self.lname}>'

#many to many relationship between users a locations, middle table that has reviews in it.
#similar to locamen table below but with its own review attribute
class Review(db.Model):
    """A review."""

    __tablename__ = "reviews"

    review_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer) #should be 1-5

    location = db.relationship("Location", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")


    def __repr__(self):
        #this sets the format of my review obj
        return f"<Review id={self.review_id} title = {self.title} body ={self.body} score = {self.score}>"


class Rating(db.Model):
    """A rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    user = db.relationship("User", back_populates="ratings")

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
