from datetime import datetime
import json
from sqlite3 import IntegrityError
from flask import flash, make_response, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import ChangePasswordForm, FeedbackForm, LoginForm, RegistrationForm, TodoForm, UpdateAccountForm
from app.utilities import save_picture
from data import skills
from app import app, os_info, current_time, users, db
from app.models import Feedback, Todo, User

@app.route('/')
def index():
    user_agent = request.user_agent
    return render_template('index.html', os_info=os_info, user_agent=user_agent, current_time=current_time)

@app.route('/about')
def about():
     return render_template('about.html')


@app.route('/skill')
@app.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        return render_template("skill.html", idx=idx, skills = skills)
    else:
        return render_template("skills.html", skills = skills)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/info')
@login_required
def info():
    name = current_user.username
    cookies = request.cookies.items()

    return render_template('info.html', name=name, cookies=cookies)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/add_cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('key')
    value = request.form.get('value')
    expiry = int(request.form.get('expiry'))

    flash('Cookie added!', 'primary')
    resp = make_response(redirect(url_for('info')))

    resp.set_cookie(key, value, max_age=expiry)

    return resp

@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    delete_key = request.form.get('delete_key')

    flash('Cookie deleted!', 'primary')
    resp = make_response(redirect(url_for('info')))

    resp.delete_cookie(delete_key)

    return resp

@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    flash('All cookies deleted!', 'primary')
    resp = make_response(redirect(url_for('info')))

    cookies = request.cookies
    for key in cookies.keys():
        resp.delete_cookie(key)

    return resp

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    form = TodoForm()
    todo_list = Todo.query.all()
    return render_template("todo.html", form=form, todo_list=todo_list)

@app.route('/add', methods=["POST"])
def add():
    form = TodoForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        new_todo = Todo(title=title, description=description, complete=False)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added successfully', 'success')
    else:
        flash('Invalid input. Please try again.', 'danger')

    return redirect(url_for("todo"))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash('Todo updated successfully', 'success')
    return redirect(url_for('todo'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = db.get_or_404(Todo, todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')
    return redirect(url_for('todo'))

@app.route('/review', methods=['GET', 'POST'])
def review():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data
        rating = form.rating.data
        feedback = Feedback(name=name, text=text, rating=rating)
        try:
            db.session.add(feedback)
            db.session.commit()
            flash('Your review added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for("review"))

    reviews = Feedback.query.all()
    return render_template("review.html", form=form, reviews=reviews)

####################################################################################################

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You already have an account!', 'success')
        return redirect(url_for('info'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account successfully created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Something went wrong', 'danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You already logged in!', 'success')
        return redirect(url_for('info'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in successfully!', 'success')
            return redirect(url_for('info'))
        else:
            flash('Invalid email or password', 'warning')
    return render_template("login.html", form=form)

@app.route('/users')
def users():
    users = User.query.all()
    total_users = len(users)
    return render_template('users.html', users=users, total_users=total_users)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    update_account_form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()

    if update_account_form.validate_on_submit():
        if update_account_form.picture.data:
            current_user.image_file = save_picture(update_account_form.picture.data)
        try:
            current_user.username = update_account_form.username.data
            current_user.email = update_account_form.email.data
            current_user.about_me = update_account_form.about_me.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
        except:
            db.session.rollback()
            flash("Failed to update!", category="danger") 
        return redirect(url_for('account'))

    elif request.method == 'GET':
        update_account_form.username.data = current_user.username
        update_account_form.email.data = current_user.email
        update_account_form.about_me.data =  current_user.about_me

    return render_template('account.html', update_account_form=update_account_form, change_password_form=change_password_form)

@app.route('/change_password', methods=['POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash("Failed to update!", category="danger")

        return redirect(url_for('account'))

    return render_template('account.html', change_password_form=form, update_account_form=UpdateAccountForm())

@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response