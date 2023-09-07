from flask import request, flash, redirect, render_template, url_for, session
from config import Config, app
from forms import MenteeForm, LoginForm, MentorForm
from models import db, Mentee, Mentor, SysAdmin, Project, ProjectStatus, ProjectCategory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import validate_csrf
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_login import current_user
from sqlalchemy import desc
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


import os
from flask_cors import CORS

app.config.from_object(Config)
db.init_app(app)


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect('/')

@app.route('/')
def home():
    return render_template('./pages/welcome_page.html')


# SIGNUP AND LOGIN FOR MENTEE

# mentee signup route



# Function to update the last active time in the session
def update_last_active_time():
    session['last_active'] = datetime.now()

# Function to check if the session has expired
def is_session_expired():
    last_active = session.get('last_active')
    if last_active and (datetime.now() - last_active) > timedelta(hours=5):
        return True
    return False

# Mentee signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = MenteeForm()

    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=5)

    if request.method == 'POST':
        if form.validate_on_submit():
            existing_mentee = Mentee.query.filter_by(email=form.email.data).first()
            if existing_mentee:
                flash('Email already registered. Please log in.')
                return redirect('/login')
            else:
                hashed_password = generate_password_hash(form.password.data)

                # Store multiple images
                images = []
                for image in request.files.getlist('images'):
                    if image.filename == '':
                        continue
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    images.append(filename)

                mentee = Mentee(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=hashed_password,
                    organization=form.organization.data,
                    age=form.age.data,
                    phone_number=form.phone_number.data,
                    education_level=form.education_level.data,
                    gender=form.gender.data,
                    program_studied=form.program_studied.data,
                    images=images
                )

                db.session.add(mentee)
                db.session.commit()

                flash('Sign up successful. Please log in.')
                return redirect('/mentee/home')
        else:
            if app.debug:  # Check if the application is running in debug mode
                print("Form validation errors:", form.errors)  # Print the form validation errors

    return render_template('./forms/mentee_signup.html', form=form)


# Mentee login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('mentee_logged_in'):
        if is_session_expired():
            flash('Session expired. Please log in again.')
            session.clear()
            return redirect('/login')
        else:
            return redirect('/')

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        mentee = Mentee.query.filter_by(email=email).first()
        if mentee and check_password_hash(mentee.password, password):
            session['mentee_logged_in'] = True
            session['last_active'] = datetime.now()
            flash('Login successful.')
            return redirect('/mentee/home')
        else:
            flash('Invalid email or password.')

    return render_template('./forms/mentee_login.html', form=form)


# Mentor signup route
@app.route('/signup/mentor', methods=['GET', 'POST'])
def mentor_signup():
    form = MentorForm()

    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=5)

    if request.method == 'POST':
        if form.validate_on_submit():
            existing_mentor = Mentor.query.filter_by(email=form.email.data).first()
            if existing_mentor:
                flash('Email already registered. Please log in.')
                return redirect('/login/mentor')
            else:
                hashed_password = generate_password_hash(form.password.data)

                # Store multiple images
                images = []
                for image in form.images.data:
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    images.append(filename)

                mentor = Mentor(
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data,
                    password=hashed_password,
                    phone_number=form.phone_number.data,
                    gender=form.gender.data,
                    age=form.age.data,
                    github_link=form.github_link.data,
                    organization=form.organization.data,
                    images=images
                )
                db.session.add(mentor)
                db.session.commit()

                flash('Sign up successful. Please log in.')
                return redirect('/mentor/home')

    return render_template('./forms/mentor_signup.html', form=form, current_user=current_user)


# Mentor login route
@app.route('/login/mentor', methods=['GET', 'POST'])
def mentor_login():
    if session.get('mentor_logged_in'):
        if is_session_expired():
            flash('Session expired. Please log in again.')
            session.clear()
            return redirect('/login')
        else:
            return redirect('/mentor/home')

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        mentor = Mentor.query.filter_by(email=email).first()
        if mentor and check_password_hash(mentor.password, password):
            session['mentor_logged_in'] = True
            session['last_active'] = datetime.now()
            flash('Login successful.')
            return redirect('/mentor/home')
        else:
            flash('Invalid email or password.')

    return render_template('./forms/mentor_login.html', form=form)


# Admin login
@app.route('/login/admin', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        if is_session_expired():
            flash('Session expired. Please log in again.')
            session.clear()
            return redirect('/login/admin')
        else:
            return redirect('/admin/home')

    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data

        sysadmin = SysAdmin.query.filter_by(email=email).first()
        if sysadmin and check_password_hash(sysadmin.password, password):
            session['admin_logged_in'] = True
            session['last_active'] = datetime.now()
            flash('Login successful.')
            return redirect('/')
        else:
            flash('Invalid email or password.')

    return render_template('./forms/admin_login.html', form=form)


# Mentor's home page
@app.route('/mentor/home')
def mentor_home():
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get("MENTORS_PER_PAGE", 5)  # Set a default value if not configured

    mentees_pagination = Mentee.query.order_by(Mentee.mentee_id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    mentees = mentees_pagination.items

    current_user = None
    if 'mentor_id' in session:
        mentor_id = session['mentor_id']
        current_user = Mentor.query.get(mentor_id)

    return render_template('./pages/mentee_home.html', mentees=mentees, current_user=current_user, pagination=mentees_pagination)



# Mentor's home details page
@app.route('/mentor/mentee/<int:mentee_id>')
def mentor_mentee_details(mentee_id):
    mentee = Mentee.query.get(mentee_id)
    return render_template('./pages/mentee_details.html', mentee=mentee)

# Mentee's home page
@app.route('/mentee/home')
def mentee_home():
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get("MENTEES_PER_PAGE", 5)  # Set a default value if not configured

    mentors_pagination = Mentor.query.order_by(Mentor.mentor_id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    mentors = mentors_pagination.items

    current_user = None
    if 'mentee_id' in session:
        mentee_id = session['mentee_id']
        current_user = Mentee.query.get(mentee_id)

    return render_template('./pages/mentor_home.html', mentors=mentors, current_user=current_user, pagination=mentors_pagination)


# Mentee's home details page
@app.route('/mentee/mentor/<int:mentor_id>')
def mentor_details(mentor_id):
    mentor = Mentor.query.get(mentor_id)
    return render_template('./pages/mentor_details.html', mentor=mentor)


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        project_status = request.form['project_status']
        project_github = request.form['project_github']
        workers = int(request.form['workers'])
        project_category = request.form['project_category']
        project_description = request.form['project_description']
        created_by = request.form['created_by']
        date_added = request.form['date_added']

        project = Project(project_name=project_name, project_status=project_status,
                          project_github=project_github, workers=workers,
                          project_category=project_category, project_description=project_description, created_by=created_by, date_added= date_added)

        db.session.add(project)
        db.session.commit()

        return 'Project created successfully!'
    
    return render_template('./forms/create_project.html')


# Route to query all available projects with pagination
@app.route('/projects', methods=['GET'])
def query_projects():
    page = request.args.get('page', 1, type=int)
    per_page = app.config.get("PROJECTS_PER_PAGE", 10)  # Set a default value if not configured

    projects_pagination = Project.query.paginate(page=page, per_page=per_page, error_out=False)
    projects = projects_pagination.items

    return render_template('./pages/projects.html', projects=projects, pagination=projects_pagination)


# Mentee edit profile route
@app.route('/mentee/edit_profile', methods=['GET', 'POST'])
def mentee_edit_profile():
    if 'mentee_id' not in session:
        flash('Please log in to access this page.')
        return redirect('/login')

    mentee_id = session['mentee_id']
    mentee = Mentee.query.get(mentee_id)

    if request.method == 'POST':
        # Update mentee profile with the form data
        mentee.first_name = request.form['first_name']
        mentee.last_name = request.form['last_name']
        mentee.phone_number = request.form['phone_number']
        mentee.organization = request.form['organization']
        mentee.age = request.form['age']
        mentee.education_level = request.form['education_level']
        mentee.program_studied = request.form['program_studied']

        db.session.commit()

        flash('Profile updated successfully.')
        return redirect('/mentee/home')

    return render_template('./forms/mentee_edit_profile.html', mentee=mentee)


# Mentee delete profile route
@app.route('/mentee/delete_profile', methods=['GET', 'POST'])
def mentee_delete_profile():
    if 'mentee_id' not in session:
        flash('Please log in to access this page.')
        return redirect('/login')

    mentee_id = session['mentee_id']
    mentee = Mentee.query.get(mentee_id)

    if request.method == 'POST':
        # Delete mentee profile
        db.session.delete(mentee)
        db.session.commit()

        session.clear()
        flash('Profile deleted successfully.')
        return redirect('/')

    return render_template('./forms/mentee_delete_profile.html', mentee=mentee)

# Mentor edit profile route
@app.route('/mentor/edit_profile', methods=['GET', 'POST'])
def mentor_edit_profile():
    if 'mentor_id' not in session:
        flash('Please log in to access this page.')
        return redirect('/login/mentor')

    mentor_id = session['mentor_id']
    mentor = Mentor.query.get(mentor_id)

    if request.method == 'POST':
        # Update mentor profile with the form data
        mentor.first_name = request.form['first_name']
        mentor.last_name = request.form['last_name']
        mentor.phone_number = request.form['phone_number']
        mentor.github_link = request.form['github_link']
        mentor.organization = request.form['organization']

        db.session.commit()

        flash('Profile updated successfully.')
        return redirect('/mentor/home')

    return render_template('./forms/mentor_edit_profile.html', mentor=mentor)


# Mentor delete profile route
@app.route('/mentor/delete_profile', methods=['GET', 'POST'])
def mentor_delete_profile():
    if 'mentor_id' not in session:
        flash('Please log in to access this page.')
        return redirect('/login/mentor')

    mentor_id = session['mentor_id']
    mentor = Mentor.query.get(mentor_id)

    if request.method == 'POST':
        # Delete mentor profile
        db.session.delete(mentor)
        db.session.commit()

        session.clear()
        flash('Profile deleted successfully.')
        return redirect('/')

    return render_template('./forms/mentor_delete_profile.html', mentor=mentor)


if __name__ == '__main__':
    app.run(debug=True)
    CORS(app)