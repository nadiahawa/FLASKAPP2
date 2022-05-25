from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, login_required, logout_user


auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth', static_folder='auth_static')


from .authforms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm()

    if request.method == 'POST':
        if lform.validate_on_submit():

            print('formdata:', lform.username.data, lform.password.data)

            user = User.query.filter_by(username=lform.username.data).first()
            print('user object from database?', user)

            if user and check_password_hash(user.password, lform.password.data):

                login_user(user)
                print('current user:', current_user.__dict__)

                flash(f'Success - you have been signed in, {user.username}.', category='success')
                return redirect(url_for('home'))

        flash(f'Incorrect username or password, please try again.', 'danger')
        return redirect(url_for('auth.login'))
    # this return statement only applies to a GET request
    return render_template('signin.html', form=lform)


@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            print('formdata:', form.data) 
            newuser = User(form.username.data, form.email.data, form.password.data, form.first_name.data, form.last_name.data)
            print('newly created user object:', newuser)
            try:

                db.session.add(newuser)
                db.session.commit()
            except:
                flash('Username or email already registered! Please try a different one.', category='danger')
                return redirect(url_for('auth.register'))
            login_user(newuser)
            flash(f'Welcome! Thank you for registering, {newuser.username}!', 'info')
            return redirect(url_for('home'))
        else: 
            flash('Sorry, passwords do not match. Please try again.', 'danger')
            return redirect(url_for('auth.register'))

    elif request.method == 'GET':
        return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('auth.login'))