from flask import Flask, render_template, request, redirect, url_for,Blueprint, flash, g, redirect,session,jsonify

from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError


from app.models import db, User ,db_update,Task

from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.routes import login_required

home = Blueprint('home', __name__)


# today_date =  datetime.now().strftime('%D-%m-%y')

# @home.route('/home')
# @login_required
# def main():
#     today_date = session.get('today_date', datetime.now().strftime('%D-%m-%y'))

#     today_name = session.get('today_name')
#     return render_template('home.html', today_date=today_date,today_name=today_name)


@home.route('/new_task')
@login_required
def new_task():
    return render_template('new_task.html')


@home.route('/create_task', methods=('GET', 'POST'))
def create_task():
    today_date = session.get('today_date', datetime.now().strftime('%D-%m-%y'))
    today_name = session.get('today_name')

    if request.method == 'POST':
        error = None

        if error is None:
            try:              
                new_task = Task(name=request.form['task'],execution_date=request.form['execution_date'])

                db.session.add(new_task)
                db.session.commit()
                
            except IntegrityError as e:
                db.session.rollback()
                if "unique constraint" in str(e):
                    error = "An error occurred."
                else:
                    error = "An error occurred."
            else:
                return redirect(url_for("home.new_task"))

        flash(error)
    # flash("Success")
    return render_template('new_task.html')


@home.route('/tasks' , methods=('GET','POST'))
@login_required
def tasks():
    today_date = session.get('today_date', datetime.now().strftime('%D-%m-%y'))
    today_name = session.get('today_name')

    tasks = Task.query.all()
    
    return render_template('home.html', tasks=tasks, today_date=today_date,today_name=today_name)



@home.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    # flash('Task deleted successfully.')
    return redirect(url_for('home.tasks'))


@home.route('/done_task/<int:task_id>', methods=['POST'])
@login_required
def done_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.isDone = True
    db.session.commit()
    # flash('Task updated successfully.')
    return redirect(url_for('home.tasks'))