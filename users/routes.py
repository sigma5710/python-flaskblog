from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from .. import db, bcrypt
from ..models import User, Post
from ..users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from ..users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)



@users.route("/register", methods=['GET', 'POST'])
def register():
    # if user tries to hardcode route in URL while being logged in
    # they will be redirected to home page
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        # hash password provided in the registration form
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # create user entity with data from the form
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        # add to the DB
        db.session.add(user)
        db.session.commit()
        # flash succes message to the user
        flash('Your account has been created! You are now able to Login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            # capture the 'next_page' in case user wanted to access the Account page
            # without being logged in
            next_page = request.args.get('next')
            
            # if user tried to reach the Account page with the URL then redirect
            # to that same page after they login
            return redirect(next_page) if(next_page) else redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful.  Check email/password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if(form.validate_on_submit()):
        # handle saving picture if the user is updating profile pic
        if(form.pic.data):
            pic_file = save_picture(form.pic.data)
            current_user.img_file = pic_file
        # current_user is currently linked with the value in the DB
        current_user.username = form.username.data
        current_user.email = form.email.data
        # commit changes
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif(request.method == 'GET'):
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static', filename=f'profile_pics/{current_user.img_file}')
    return render_template('account.html', title='Account',
                            img_file=img_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user) \
                .order_by(Post.date_posted.desc()) \
                .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    # make sure there is no one logged in
    # in order to attempt password reset
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    if(form.validate_on_submit()):
        # get user based on the email user submitted
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',
                            form=form)

@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if(current_user.is_authenticated):
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    if(user is None):
        flash('That is an invalid/expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if(form.validate_on_submit()):
        # hash password provided in the registration form
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        # flash succes message to the user
        flash('Your password has been updated! You are now able to Login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password',
                            form=form)