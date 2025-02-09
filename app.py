from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)

# 🔑 Session & Security Configurations
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SESSION_TYPE"] = "filesystem"  # Fix session persistence issues

# 📌 Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///your_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 💂️ Upload Folder for Profile Pictures
UPLOAD_FOLDER = "static/uploads/profile_pics"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 🔗 Initialize Database
db = SQLAlchemy(app)

# 🔑 Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect if not logged in
login_manager.session_protection = "strong"

# 🎭 User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed Password
    profile_pic = db.Column(db.String(300), default="static/uploads/profile_pics/default.png")
    is_admin = db.Column(db.Boolean, default=False)

# 📌 Create Tables in Database
with app.app_context():
    db.create_all()

# 🔄 Flask-Login: Load User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 🏠 Home Page
@app.route("/")
def home():
    return render_template("index.html")

# 🔐 Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        profile_pic = request.files.get("profile_pic")

        # Check if email exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        # Hash Password
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        # Handle Profile Picture Upload
        profile_pic_path = "static/uploads/profile_pics/default.png"
        if profile_pic and profile_pic.filename:
            filename = secure_filename(f"{uuid.uuid4()}_{profile_pic.filename}")  # Unique filename
            profile_pic.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            profile_pic_path = os.path.join("static/uploads/profile_pics", filename)

        # Save User to Database
        new_user = User(username=username, email=email, password=hashed_password, profile_pic=profile_pic_path)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Try again!", "danger")

    return render_template("register.html")

# 🔑 Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Fetch User
        user = User.query.filter_by(email=email).first()

        # Validate Password
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials. Please try again.", "danger")
            return redirect(url_for("login"))

        # Log the user in
        login_user(user)
        flash("Login successful!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")

# 🏠 Dashboard (Only for Logged-in Users)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username, profile_pic=current_user.profile_pic)

# 🔐 Admin Dashboard
@app.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("Access Denied! Admins only.", "danger")
        return redirect(url_for("dashboard"))

    users = User.query.all()
    return render_template("admin.html", users=users)

# 🔓 Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# 🚀 Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
