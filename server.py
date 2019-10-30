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


@app.route('/register_user', methods = ["POST"])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')
    is_avial = User.query.filter_by(email=email).first()
    if is_avial is None:

        new_user = User(email=email,
                        password=password,
                        age=age,
                        zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
    else:
        flash('THis user already exists')
        return redirect('/register')

    return redirect('/')


@app.route('/loginPage')
def log_in_page():
    return render_template('login.html')


@app.route('/login')
def log_in():
    email = request.args.get('email')
    password = request.args.get('password')
    is_avial = User.query.filter_by(email=email).first()
    print(is_avial.password)

    if (is_avial is None) or (is_avial.password != password):
        flash('Please enter correct email id or password.')
        return redirect('/loginPage')
    else:
        flash('You are successfully logged in.....')
        session['id'] = email

        return redirect('/userpage')


@app.route('/userpage')
def userpage():
    user= User.query.filter_by(email = session.get('id'))
    return render_template('userPage.html',record=user)

    
@app.route('/logout')
def logged_out():
    flash('You are logged out')
    session.pop('id')
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
