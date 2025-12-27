import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from peewee import Model, CharField, SqliteDatabase
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- Flask App --------------------
app = Flask(__name__)
app.secret_key = "secret_key_123"

# -------------------- Database --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = SqliteDatabase(os.path.join(BASE_DIR, "database.db"))

# -------------------- User Model --------------------
class User(Model, UserMixin):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

db.connect(reuse_if_open=True)
db.create_tables([User], safe=True)

# -------------------- Login Manager --------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

# -------------------- Home Page --------------------
@app.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

# -------------------- Register --------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        User.create(
            username=username,
            password=hashed_password
        )

        return redirect(url_for("login"))

    return render_template("register.html")

# -------------------- Login --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            user = User.get(User.username == username)
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("home"))
        except User.DoesNotExist:
            pass

    return render_template("login.html")

# -------------------- Logout --------------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=True)
