from app.__inti__ import app, db
from flask import render_template, url_for, redirect, request, flash
from app.form import AddTaskForm, SiginForm, LoginForm
from flask_login import current_user, logout_user, login_user, login_required
from app.models import User, Task
from werkzeug.urls import url_parse


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = AddTaskForm()
    if form.validate_on_submit():
        list = Task(task=form.new_task.data, is_complete=False)
        current_user.addTask(list)
        db.session.commit()
        return redirect('/index')
    lists = current_user.task.filter_by(is_complete = False).all()
    completed_lists = current_user.task.filter_by(is_complete = True).all()
    print(current_user.task.all())
    print(lists)
    print(completed_lists)

    return render_template('index.html', lists=lists, completed_lists=completed_lists, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('main')


@app.route('/remove_task', methods=['GET', 'POST'])
def remove_task():
    item_id = int(request.form.get("item_id"))
    Task.query.filter_by(id=item_id).delete()

    print(item_id)
    db.session.commit()

    # print(task)
    # current_user.removeTask(task)
    return redirect('/index')

@app.route('/', methods=['GET', 'POST'])

@app.route('/main', methods=['GET', 'POST'])
def main():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SiginForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('main.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main'))
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/completed_task', methods=['GET', 'POST'])
def completed_task():
    item_id_completed = int(request.form.get("item_id_completed"))
    print(item_id_completed)
    item = current_user.task.filter_by(id=item_id_completed).first()
    item.is_complete = not item.is_complete
    db.session.commit()

    return redirect('/index')
