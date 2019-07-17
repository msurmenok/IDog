from flask import (render_template, redirect, url_for, flash, request, Flask,
                   send_from_directory)
from werkzeug.utils import secure_filename
from __init__ import app, db
from model.load_model import run_model
from forms import RegistrationForm, LoginForm
from dbmodel import User, Favorites, Dogs
from flask_login import login_user, login_required, logout_user, current_user
from wtforms import validators

import os
import geoip2.database
from petfinder import PetFinderClient

os.environ['PYTHONPATH'] = os.getcwd()
# UPLOAD_FOLDER = "/static"
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             'static/tmp')
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

petfinder = PetFinderClient()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_zipcode(request):
    """ Find zip code based on user ip using geoip2 library.
        If can't find zip code for provided ip, return zip code for SJSU
    """
    user_ip = request.access_route[0]
    reader = geoip2.database.Reader(
        os.path.dirname(os.path.abspath(__file__)) +
        '/geolite2/GeoLite2-City.mmdb')
    try:
        response = reader.city(user_ip)
        return response.postal.code
    except geoip2.errors.AddressNotFoundError:
        return '95192'


@app.route('/', methods=['GET', 'POST'])
def index():
    zipcode = get_zipcode(request)
    # If user logged in, get all his favorite dogs
    fav_dogs = []
    if current_user.is_authenticated:
        fav_dogs = [dog.dog_id for dog in User.query.filter_by(id=current_user.id).first().favs]
    if request.method == 'POST':
        if 'zipcode' in request.form:
            zipcode = request.form['zipcode']
        if len(zipcode) != 5 or not zipcode.isdigit():
            flash('Please input a valid zipcode')
            return redirect(request.url)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash('No selected file')
            # return redirect(request.url)
            dogs = petfinder.get_dogs(zipcode)
            return render_template("index.html", zipcode=zipcode, dogs=dogs)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            prediction = run_model(os.path.join(UPLOAD_FOLDER, filename))

            if 'zipcode' in request.form:
                # zipcode = request.form['zipcode']
                zipcode = 94065  # default
                dogs = petfinder.get_dogs_by_breed("labrador retriever", zipcode)
                # dogs = petfinder.get_dogs_by_breed()  # default german shepard, 94065
                dog = dogs[0]

            return render_template("index.html",
                                   breed=prediction,
                                   path=filename,
                                   name=dog.name,
                                   dogpath=dog.photo_thumbnail,
                                   phone=dog.phone,
                                   zipcode=zipcode,
                                   testdog=dog,
                                   dogs=dogs,
                                   fav_dogs=fav_dogs
                                   )
    dogs = petfinder.get_dogs(zipcode)
    return render_template('index.html', zipcode=zipcode, dogs=dogs, fav_dogs=fav_dogs)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        try:
            form.check_email(form.email)
            flash("Thank for registration!")
        except validators.ValidationError as e:
            flash(str(e))
            return redirect(url_for('signup'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in Successfully')
            next = request.args.get('next')
            if next is None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)

        else:
            flash('Your email or password doesn\'t match the record')
    return render_template('login.html', form=form)


@app.route('/my_dogs/')
def user_fav_page():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    # grab the first user or return a 404 page
    return render_template('welcome.html', user=user)


@app.route('/dog/<dog_id>')
def check_out_dog(dog_id):
    dog = petfinder.get_dog_by_id(dog_id)
    return render_template('dog.html', dog=dog)


@app.route('/like/<int:dog_id>')
@login_required
def like_dog(dog_id):
    # Get all user dogs
    user_dogs = User.query.filter_by(id=current_user.id).first().favs
    user_dogs_ids = [dog.dog_id for dog in user_dogs]

    # Get all existing dogs
    all_dogs = Dogs.query.all()
    all_dogs_ids = [dog.dog_id for dog in all_dogs]

    # If dog is not in database yet, add it
    if dog_id not in all_dogs_ids:
        dog_data = petfinder.get_dog_by_id(dog_id)
        new_dog = Dogs(
            dog_id=dog_id,
            dog_name=dog_data.name,
            dog_gender=dog_data.gender,
            dog_age=dog_data.age,
            dog_pic=dog_data.photo_thumbnail
        )
        db.session.add(new_dog)
        db.session.commit()
    # If user already like this dog, remove from Favorites, otherwise add to favorites

    if dog_id not in user_dogs_ids:
        new_fav = Favorites(
            user_id=current_user.id,
            dog_id=dog_id
        )
        db.session.add(new_fav)
    else:
        old_fav = Favorites.query.filter_by(user_id=current_user.id).filter_by(dog_id=dog_id).first()
        db.session.delete(old_fav)
    db.session.commit()
    print(User.query.filter_by(id=current_user.id).first().favs)
    return redirect((url_for('index')))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect((url_for('index')))


if __name__ == '__main__':
    app.run(debug=True)
