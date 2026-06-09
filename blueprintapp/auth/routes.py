from flask import Blueprint, request, redirect, flash, render_template, url_for
from flask_login import login_user, logout_user, login_required
from blueprintapp.auth.models import User
from blueprintapp.app import db, bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder='templates')

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Usuario ya existe","danger")
            return redirect(url_for("auth.register"))
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            flash("Usuario logueado ", "success")
            return redirect(url_for("bp_core.index"))
        flash("Usuario y/o contraseña incorrectas","danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("bp_core.index"))