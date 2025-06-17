from flask import Blueprint, session, redirect, render_template, url_for, request, flash
from app import db
from app.models import Task, User

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def home():
    return render_template('home.html')


@tasks_bp.route('/view')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(username=session['user']).first()
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('tasks.html', tasks=tasks)


@tasks_bp.route('/add', methods=["POST"])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    title = request.form.get('title')

    if title and user:
        new_task = Task(title=title, status="Pending", user_id=user.id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task Added Successfully', 'success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    task = Task.query.get(task_id)

    if task and task.user_id == user.id:
        if task.status == 'Pending':
            task.status = 'Working'
        elif task.status == 'Working':
            task.status = 'Done'
        else:
            task.status = 'Pending'
        db.session.commit()
    else:
        flash('Unauthorized action or task not found!', 'danger')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods=["POST"])
def clear_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    Task.query.filter_by(user_id=user.id).delete()
    db.session.commit()
    flash('All Tasks Cleared!', 'info')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=session['user']).first()
    task = Task.query.get(task_id)

    if task and task.user_id == user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'info')
    else:
        flash('Unauthorized or task not found!', 'danger')

    return redirect(url_for('tasks.view_tasks'))
