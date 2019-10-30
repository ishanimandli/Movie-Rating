"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, redirect, flash,session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Rating


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route('/users')
def user_list():
    users= User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register')
def register_form():
    return render_template("registration.html")

@app.route('/register', methods = ["POST"])
def register_user():
    email = request.form('email')
    password = request.form('password')
    age = request.form('age')
    zipcode = request.form('zipcode')
    new_user = User(email=email,
                    password=password,
                    age=age,
                    zipcode=zipcode)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')