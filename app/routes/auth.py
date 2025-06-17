from flask import Blueprint,session,render_template,url_for,redirect,request,flash
from app.models import User
from app import db

auth_bp=Blueprint('auth',__name__)
# ------------------ LOGIN ------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user"] = user.username
            flash('Login Successful', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash("Invalid Username or Password", "danger")

    return render_template('login.html')


# ------------------ REGISTER ------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists", "warning")
            return redirect(url_for('auth.register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user',None)
    flash('Logged out','info')
    return redirect(url_for('auth.login'))