import functools

from flask import Flask, render_template, request, redirect, url_for,Blueprint, flash, g, redirect,session,jsonify
import random
from app.models import db, User ,db_update
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError

from datetime import datetime, timedelta

from .helper  import send_password_reset_email, is_email_exists


today_date = datetime.now()
# Get the day of the week (Monday is 0 and Sunday is 6)
day_of_week = today_date.weekday()

# You can use a list to map the numeric representation to the day name
days_of_week_en = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

days_of_week = ['שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת', 'ראשון']
day_name = days_of_week[day_of_week]


# auth = Blueprint('auth', __name__, url_prefix='/auth')
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email!'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password!'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['today_date'] = today_date.strftime('%d-%m-%Y')
            session['today_name'] = day_name

            return redirect(url_for('home.tasks'))
        flash(error)

    return render_template('auth/login.html')



@auth.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data = {
            'Fname':request.form['Fname'],
            'Lname' : request.form['Lname'],
            'phone' : request.form['phone'],
            'email' : request.form['email'],
            'b_date' : request.form['b_date'],            
            'password' : request.form['password'],
        }
        error = None

        for fields in data:
            if not fields:
                error = "all fields required"

        if error is None:
            try:              
                # Create a new user instance with the org_id obtained from the URL parameter
                new_user = User(Fname=data['Fname'] ,Lname=data['Lname'] ,phone=data['phone'] ,email=data['email'], b_date=data['b_date'] ,password=generate_password_hash(data['password']))

                # Add the new user to the database
                db.session.add(new_user)
                db.session.commit()

                #giv the user a user defoult role
                # user_role = UserRole(user_id=new_user.id,role_id = '2')
                
                # Add the new user_role to the database
                # db.session.add(user_role)
                # db.session.commit()
                
            except IntegrityError as e:
                db.session.rollback()
                # Check if the error message indicates a unique constraint violation
                if "unique constraint" in str(e):
                    error = f"User with email {data['email']} is already registered."
                else:
                    # If it's a different IntegrityError, handle it accordingly
                    error = "An error occurred during registration."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')




@auth.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    if request.method == 'POST':
        error = None
        user_email = request.form['email']
        if is_email_exists(user_email):
            temp_password = str(random.randint(10000000,90000000))
            send_password_reset_email(user_email,temp_password)
            user = User.query.filter_by(email = user_email).first()
            if user:
                user.password = generate_password_hash(temp_password)
                db.session.commit()
                return redirect('login')
                # return jsonify("success:temp password sended")
            else:
                error = "User not fpund"
                flash(error)
        else:
            error = "Email does not exist"
            flash(error)
        
    return render_template('auth/reset_password.html')





@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id = user_id).first()




def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view




@auth.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

