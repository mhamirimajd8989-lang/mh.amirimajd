from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from peewee import Model, CharField, SqliteDatabase

app = Flask(__name__)
app.secret_key = "secret_key_123"

# دیتابیس
db = SqliteDatabase("database.db")

# مدل کاربر
class User(Model, UserMixin):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

# ساخت جدول
db.connect()
db.create_tables([User])

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.get_by_id(user_id)
    except:
        return None

# صفحه اصلی
@app.route("/")
def home():
    return "Flask + Peewee OK ✅"

# ثبت نام
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.select().where(User.username == username).exists():
            return "این نام کاربری قبلاً ثبت شده"

        User.create(username=username, password=password)
        return redirect(url_for("login"))

    return render_template("register.html")

# لاگین
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        remember = True if request.form.get("remember") else False

        try:
            user = User.get(User.username == username)
            if user.password == password:
                login_user(user, remember=remember)
                return redirect(url_for("dashboard"))
            else:
                return "رمز عبور اشتباه است"
        except:
            return "کاربر وجود ندارد"

    return render_template("login.html")

# داشبورد
@app.route("/dashboard")
@login_required
def dashboard():
    return "خوش آمدی! لاگین شدی 🎉"

# خروج
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
