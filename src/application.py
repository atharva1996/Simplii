from datetime import datetime, timedelta
from smtplib import SMTPException
from bson.objectid import ObjectId
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
import pytz
from werkzeug.security import generate_password_hash
import schedule
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from tabulate import tabulate
from flask_wtf import form
from flask import app, render_template, session, url_for, flash, redirect, request, Response, Flask
from flask_pymongo import PyMongo
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
from pymongo import ASCENDING
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm, UpdateForm
import bcrypt
import os
import csv
import sys

from flask_login import LoginManager, login_required

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii'
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "dummysinghhh@gmail.com"
app.config['MAIL_PASSWORD'] = "wbjf dsfu mper nqfv"
mail = Mail(app)

# Initialize the URLSafeTimedSerializer with your secret key and a salt
serializer = URLSafeTimedSerializer(app.secret_key, salt='password-reset')

scheduler = BackgroundScheduler()

def fetch_tasks():
    print("fetch_tasks called")
    # Calculate the current date
    current_date = datetime.now().date()

    # Calculate the date 7 days from now
    seven_days_later = current_date + timedelta(days=7)

    users = mongo.db.users.find()
    with app.app_context():  # Create an application context
        for u in users:
            relevant_tasks = mongo.db.tasks.find({
                'user_id': u['_id'],
                'duedate': {
                    # '$gte': current_date.strftime('%Y-%m-%d'),
                    '$lte': seven_days_later.strftime('%Y-%m-%d')
                }
            }).sort('duedate', 1)

            tasksListContent = list(relevant_tasks)

            table_html = "<table border='1'><tr><th>Task Name</th><th>Category</th><th>Start Date</th><th>Due Date</th><th>Status</th><th>Hours</th></tr>"
            for user_tasks in tasksListContent:
                # Create an HTML table from the task data
                table_html += f"<tr><td>{user_tasks['taskname']}</td><td>{user_tasks['category']}</td><td>{user_tasks['startdate']}</td><td>{user_tasks['duedate']}</td><td>{user_tasks['status']}</td><td>{user_tasks['hours']}</td></tr>"
            table_html += "</table>"

            # Compose the email
            msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[u['email']])

            # Create the text version of the email with the table
            email_body = f"Here are your tasks due in next 7 days:\n\n{table_html}"
            msg.html = email_body
            try:
                mail.send(msg)  # Attempt to send the email
                print(f"Email sent to {u['email']} successfully.")
            except SMTPException as e:
                # Handle SMTP errors
                print(f"Failed to send email to {u['email']}. Error: {str(e)}")
            except Exception as e:
                # Handle other exceptions
                print(f"An error occurred while sending an email to {u['email']}. Error: {str(e)}")


    # flash("Email reminders sent for tasks with due dates in the specified range.", 'success')
    print('***************')

@app.route("/")
@app.route("/home")
def home():
    ############################
    # home() function displays the homepage of our website.
    # route "/home" will redirect to home() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the login page
    # ##########################
    if session.get('email'):
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# Reset Password route
@app.route("/resetPassword/<token>", methods=['GET', 'POST'])
def resetPassword(token):
    if request.method == 'GET':
        try:
            # Verify the token and get the associated email
            email = serializer.loads(token, max_age=3600)  # Max age in seconds (1 hour)

            # Here, you can add code to identify the user by their email and present a password reset form
            # For example, you can store the email in a session or a hidden form field to ensure it's the same user

            return render_template('resetPassword.html', email=email)

        except SignatureExpired:
            flash('The password reset link has expired.', 'error')
            return redirect(url_for('forgotPassword'))
        except BadSignature:
            flash('Invalid password reset link.', 'error')
            return redirect(url_for('forgotPassword'))

    elif request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        # Update the user's password in the database
        user = mongo.db.users.find_one({'email': email})
        if user:
            user_id = user['_id']
            # Update the password for the user with the specified ID
            mongo.db.users.update_one(
                {"_id": user_id},
                {"$set": {"pwd": new_password}}
            )

            flash('Password reset successful. You can now log in with your new password.', 'success')
            return redirect(url_for('login'))

    return render_template('resetPassword.html')

# Handle cases where the user is not found or the old password doesn't match
# You can redirect to an appropriate page or display an error message.

@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPassword():
    ############################
    # forgotPassword() redirects the user to dummy template.
    # route "/forgotPassword" will redirect to forgotPassword() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the dummy page
    # ##########################
    if not session.get('user_id'):
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                email = request.form.get('email')
                # id = mongo.db.users.find_one({'email': email})
                user = mongo.db.users.find_one({'email': email})



                if user:
                    # Generate a reset token
                    reset_token = serializer.dumps(email, salt='password-reset')

                    # Store the reset token in the user's document in the database
                    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'reset_token': reset_token}})

                    # Send a reset password email
                    reset_link = url_for('resetPassword', token=reset_token, _external=True)
                    msg = Message('Password Reset', sender=app.config['MAIL_USERNAME'], recipients=[email])
                    msg.body = f'Visit the following link to reset your password: {reset_link}'
                    mail.send(msg)

                    flash('Password reset link sent to your email.', 'info')
                else:
                    flash('Email address not found.', 'error')
        
    else:
        return redirect(url_for('home'))
    return render_template('forgotPassword.html', title='Register', form=form)


@app.route("/recommend")
def recommend():
    ############################
    # recommend() function opens the task_recommendation.csv file and displays the data of the file
    # route "/recommend" will redirect to recommend() function.
    # input: The function opens the task_recommendation.csv
    # Output: Our function will redirect to the recommend page for showing the data
    # ##########################
   

    if session.get('user_id'):
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)

        # Fetch all tasks for the user and sort by 'duedate' in ascending order
        tasks = list(mongo.db.tasks.find({'user_id': user_id}).sort('duedate', ASCENDING))
        return render_template('recommend.html', title='Recommend', tasks=tasks)
    else:
        return redirect(url_for('home'))
    



@app.route("/send_email_reminders", methods=['GET', 'POST'])
def send_email_reminders():
    if session.get('user_id'):
        if request.method == 'POST':
            due_date = request.form.get('duedate')  # Get the due date input from the form
            user_str_id = session.get('user_id')
            user_id = ObjectId(user_str_id)
            
            # Convert the due date to a datetime object
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date()

            # Fetch tasks whose due date falls within the specified range
            relevant_tasks = mongo.db.tasks.find({
                'user_id': user_id,
                'duedate': {'$lt': due_date.strftime('%Y-%m-%d')}  # Convert due_date back to string for comparison
            }).sort('duedate', 1)

            # Convert the cursor to a list of dictionaries
            relevant_tasks = list(relevant_tasks)

            # Create an HTML table from the task data
            table_html = "<table border='1'><tr><th>Task Name</th><th>Category</th><th>Start Date</th><th>Due Date</th><th>Status</th><th>Hours</th></tr>"

            for task in relevant_tasks:
                table_html += f"<tr><td>{task['taskname']}</td><td>{task['category']}</td><td>{task['startdate']}</td><td>{task['duedate']}</td><td>{task['status']}</td><td>{task['hours']}</td></tr>"

            table_html += "</table>"

            # Compose the email
            email= session.get('email')
            msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[email])

            # Create the text version of the email with the table
            email_body = f"Here are your tasks:\n\n{table_html}"
            msg.html = email_body
            mail.send(msg)

            flash("Email reminders sent for tasks with due dates in the specified range.", 'success')
            return render_template('recommend.html', title='Recommend', tasks=relevant_tasks)
        
        # Handle GET request, presumably to display tasks
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        tasks = mongo.db.tasks.find({
            'user_id': user_id,
        })
        return render_template('recommend.html', tasks=tasks)
    else:
        return redirect(url_for('home'))




@app.route("/dashboard")
def dashboard():
    ############################
    # dashboard() function displays the tasks of the user
    # route "/dashboard" will redirect to dashboard() function.
    # input: The function takes session as the input and fetches user tasks from Database
    # Output: Our function will redirect to the dashboard page with user tasks being displayed
    # ##########################
    tasks = ''
    print('session in dashboard ',session)
    if session.get('user_id'):
        tasks = mongo.db.tasks.find({'user_id': ObjectId(session.get('user_id'))})
    return render_template('dashboard.html', tasks=tasks)

@app.route("/about")
def about():
    # ############################
    # about() function displays About Us page (about.html) template
    # route "/about" will redirect to about() function.
    # ##########################
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # ############################
    # register() function displays the Registration portal (register.html) template
    # route "/register" will redirect to register() function.
    # RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
    # Input: Username, Email, Password, Confirm Password
    # Output: Value update in database and redirected to home login page
    # ##########################
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')
                mongo.db.users.insert_one({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()), 'tasksList':[], 'temp': None})
                msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[email])
                msg.body = f"Hey {username},\n\n" \
                "We're excited to welcome you to Simplii, your new task scheduling companion. Simplii is here to help you stay organized, meet deadlines, and achieve your goals efficiently.\n\n" \
                "With Simplii, you can schedule your tasks, set deadlines, and work on them with ease. Never miss an important deadline again!\n\n" \
                "Thank you for choosing Simplii. We're thrilled to have you on board. If you have any questions or need assistance, feel free to reach out to us.\n\n" \
                "Best regards,\n" \
                "The Simplii Team"
                mail.send(msg)
                print("Message sent!")
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/deleteTask", methods=['GET', 'POST'])
def deleteTask():
    ############################
    # deleteTask() function will delete the particular user task from database.
    # route "/deleteTask" will redirect to deleteTask() function.
    # input: The function takes email, task, status, category as the input and fetches from the database
    # Output: Out function will delete the particular user task from database
    # ##########################
    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        print("task, status, category ", task, status, category)
        id = mongo.db.tasks.find_one(
            {'user_id': user_id, 'taskname': task, 'status': status, 'category': category}, {'_id'})
        print("id in delete task ",id)
        mongo.db.tasks.delete_one({'_id': id['_id']})
        return "Success"
    else:
        return "Failed"


@app.route("/task", methods=['GET', 'POST'])
def task():
    # ############################
    # task() function displays the Add Task portal (task.html) template
    # route "/task" will redirect to task() function.
    # TaskForm() called and if the form is submitted then new task values are fetched and updated into database
    # Input: Task, Category, start date, end date, number of hours
    # Output: Value update in database and redirected to home login page
    # ##########################
    if session.get('user_id'): 
        form = TaskForm()
        if form.validate_on_submit():
            print("inside form")
            if request.method == 'POST':
                user_str_id = session.get('user_id')
                user_id = ObjectId(user_str_id)
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                task_id = mongo.db.tasks.insert({'user_id': user_id,
                                       'taskname': taskname,
                                       'category': category,
                                       'startdate': startdate,
                                       'duedate': duedate,
                                       'status': status,
                                       'hours': hours})
                
                #Now update the user schema's TaskList field with the taskId(Basically append the new task id to that array)
                user_document = mongo.db.users.find_one({'_id': user_id})
                tasks_list = user_document.get('tasksList', [])
                tasks_list.append(task_id)

                # Update the user's tasksList field
                mongo.db.users.update_one(
                    {'_id': user_id},
                    {
                        '$set': {'tasksList': tasks_list}
                    }
                )
            flash(f' {form.taskname.data} Task Added!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('task.html', title='Task', form=form)


@app.route("/editTask", methods=['GET', 'POST'])
def editTask():
    ############################
    # editTask() function helps the user to edit a particular task and update in database.
    # route "/editTask" will redirect to editTask() function.
    # input: The function takes email, task, status, category as the input
    # Output: Out function will update new values in the database
    # ##########################
    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        id = mongo.db.tasks.find_one(
            {'user_id': user_id, 'taskname': task, 'status': status, 'category': category})
        print("id in edit task ", id)
        return json.dumps({'taskname': id['taskname'], 'category': id['category'], 'startdate': id['startdate'], 'duedate': id['duedate'], 'status': id['status'], 'hours': id['hours']}), 200, {
            'ContentType': 'application/json'}
    else:
        return "Failed"


@app.route("/updateTask", methods=['GET', 'POST'])
def updateTask():
    ############################
    # updateTask() function displays the updateTask.html page for updations
    # route "/updateTask" will redirect to updateTask() function.
    # input: The function takes variious task values as Input
    # Output: Out function will redirect to the updateTask page
    # ##########################
    if session.get('user_id'):
        print("params in updateTask ", request.url)
        params = request.url.split('?')[1].split('&')
        for i in range(len(params)):
            params[i] = params[i].split('=')
        for i in range(len(params)):
            if "%" in params[i][1]:
                index = params[i][1].index('%')
                params[i][1] = params[i][1][:index] + \
                    " " + params[i][1][index + 3:]
        d = {}
        for i in params:
            d[i[0]] = i[1]

        form = UpdateForm()

        form.taskname.data = d['taskname']
        form.category.data = d['category']
        form.status.data = d['status']
        form.hours.data = d['hours']
        
        # Assuming that 'd['startdate']' and 'd['duedate']' are date strings in a format like 'YYYY-MM-DD'
        # Convert them to datetime objects
        startdate_str = d['startdate']
        duedate_str = d['duedate']
        # Convert to datetime objects
        startdate_datetime = datetime.strptime(startdate_str, '%Y-%m-%d')
        duedate_datetime = datetime.strptime(duedate_str, '%Y-%m-%d')

        # Now, set the datetime objects in the form
        form.startdate.data = startdate_datetime
        form.duedate.data = duedate_datetime
        

        if form.validate_on_submit():
            if request.method == 'POST':
                user_str_id = session.get('user_id')
                user_id = ObjectId(user_str_id)
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                mongo.db.tasks.update({'user_id': user_id, 'taskname': d['taskname'], 'startdate': d['startdate'], 'duedate': d['duedate']},
                                      {'$set': {'taskname': taskname, 'startdate': startdate, 'duedate': duedate, 'category': category, 'status': status, 'hours': hours}})
            flash(f' {form.taskname.data} Task Updated!', 'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))
    return render_template('updateTask.html', title='Task', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # ############################
    # login() function displays the Login form (login.html) template
    # route "/login" will redirect to login() function.
    # LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
    # Input: Email, Password, Login Type
    # Output: Account Authentication and redirecting to Dashboard
    # ##########################
    if not session.get('user_id'):
        form = LoginForm()
        if form.validate_on_submit():
            temp = mongo.db.users.find_one({'email': form.email.data}, {
                'email', 'name', 'pwd'})
            print("temp ", temp)
            if temp is not None and temp['email'] == form.email.data and (
                bcrypt.checkpw(
                    form.password.data.encode("utf-8"),
                    temp['pwd'])): #or temp['temp'] == form.password.data
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                session['name'] = temp['name']
                session['user_id'] = str(temp['_id'])
                return redirect(url_for('dashboard'))
            else:
                flash(
                    'Login Unsuccessful. Please check username and password',
                    'danger')
    else:
        print("session details ", session)
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # ############################
    # logout() function just clears out the session and returns success
    # route "/logout" will redirect to logout() function.
    # Output: session clear
    # ##########################
    session.clear()
    return "success"


@app.route("/dummy", methods=['GET'])
def dummy():
    # ############################
    # dummy() function performs the functionality displaying the message "feature will be added soon"
    # route "/dummy" will redirect to dummy() function.
    # Output: redirects to dummy.html
    # ##########################
    """response = make_response(
                redirect(url_for('home'),200),
            )
    response.headers["Content-Type"] = "application/json",
    response.headers["token"] = "123456"
    return response"""
    return "Page Under Maintenance"

if __name__ == '__main__':
    scheduler.add_job(func=fetch_tasks, trigger="cron", day_of_week = "*", hour = 00, minute = 00)
    scheduler.start()
    app.run(debug=True, use_reloader = False)