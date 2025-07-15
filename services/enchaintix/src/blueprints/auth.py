from flask import Blueprint, request, url_for, render_template, redirect, make_response
from flask_login import login_user, logout_user
from models.user import User

auth = Blueprint('auth routes', __name__)

@auth.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if not (username or password):
        return redirect("/")

    user = User.auth(username, password)
    
    if not user:
        user = User.get_by_username(username)
        response = make_response(redirect('/'))
        if user != None:
            response.set_cookie('forgor', username)
        
        return response

    login_user(user)
    return  redirect("/")

@auth.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    secret_word = request.form.get("secret_word", "")
    if not (username or password):
        return redirect("/")

    user = User.register(username, password, secret_word)
    
    if not user:
        return redirect("/")

    login_user(user)
    return  redirect("/")

@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/")
