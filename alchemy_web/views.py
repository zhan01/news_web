import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from alchemy_web import app, db, bcrypt
from alchemy_web.forms import Form, RegistrationForm, LoginForm, UpdateAccountForm, InterestForm
from alchemy_web.models import User, Interest, user_schema, users_schema, interest_schema, interests_schema
from flask_login import login_user, current_user, logout_user, login_required
import json


@app.route("/")
@app.route("/test")
def home():
   
    interest = Interest.query.all()
    interest_json = interests_schema.dump(interest).data
    interest = json.dumps(interest_json)
    return render_template('home.html', interests=interest)


@app.route("/business")
def business():
    return render_template('business.html', title='Business')
    

@app.route("/health")
def health():
    return render_template('health.html', title='Health')

@app.route("/entertainment")
def entertainment():
    return render_template('entertainment.html', title='Entertainment')

@app.route("/sport")
def sport():
    return render_template('sport.html', title='Sport')

@app.route("/tech")
def tech():
    return render_template('tech.html', title='Tech')

@app.route("/index")
def index():
    return render_template('index.html', title='Index')

@app.route("/science")
def science():
    
    return render_template('scince.html', title='Science')

@app.route("/youtube")
def youtube():
    interest = Interest.query.all()
    interest_json = interests_schema.dump(interest).data
    interest = json.dumps(interest_json)
    
    return render_template('youtube.html', interests=interest)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/images/profile_pics/', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    interests = Interest.query.filter_by(user_id=current_user.id)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='images/profile_pics/' + current_user.image_file)
    return render_template('dashboard.html', title='Account',
                           image_file=image_file, form=form, interests=interests)


@app.route("/interest", methods=['GET', 'POST'])
@login_required
def log_interest():
    form = InterestForm()
    if form.validate_on_submit():
        interest = Interest(content=form.content.data, user=current_user)
        db.session.add(interest)
        db.session.commit()
        flash('Interest Added!', 'success')
        return redirect(url_for('log_interest'))
    return render_template('log_interests.html', title='Explore', form=form)


@app.route("/interest/<int:interest_id>/delete", methods=['POST'])
@login_required
def delete_interest(interest_id):
    interest = Interest.query.get_or_404(interest_id)
    if interest.user != current_user:
        abort(403)
    db.session.delete(interest)
    db.session.commit()
    flash('Interest Removed', 'success')
    return redirect(url_for('dashboard'))
