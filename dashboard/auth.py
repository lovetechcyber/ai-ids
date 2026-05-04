from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

# Demo user (hashed password)
users = {
    "admin": bcrypt.generate_password_hash("admin123").decode("utf-8")
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and bcrypt.check_password_hash(users[username], password):
            login_user(User(username))
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "error")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))