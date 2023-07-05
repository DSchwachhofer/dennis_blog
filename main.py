from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

from scripts.forms import ContactForm, LoginForm, RegisterForm, NewPostForm
from scripts.email import Email_Handler
from scripts.db_handler import db, Db_Handler

from datetime import date
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

db_handler = Db_Handler()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db.init_app(app)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db_handler.get_user_from_id(user_id)

# creating database
# with app.app_context():
#     db.create_all()

# check if user is admin (id = 1)
def check_for_admin():
    user_id = 0
    if current_user.is_authenticated:
        user_id = current_user.id
    if user_id==1:
        return True
    else:
        return False

# add a current year variable which will be accessed from all sites.
@app.context_processor
def inject_current_year():
    return {"current_year": date.today().year}


@app.route("/")
def home():
    # set up dynamic titles for home route.
    title = request.args.get("new_title", "")
    if not title:
        title = "Dennis's Blog"
    subtitle = request.args.get("new_subtitle")
    if not subtitle:
        subtitle = "a collection of random musings."

    all_posts = db_handler.get_all_posts()
    return render_template("index.html", page="home", title=title, subtitle=subtitle, image_url=url_for('static', filename='images/banner-home.jpg'), posts=all_posts, logged_in=current_user.is_authenticated, is_admin=check_for_admin())

@app.route("/login", methods=["GET", "POST"])
def login():
    title = request.args.get("new_title", "")
    if not title:
        title = "Welcome Back"
    subtitle = request.args.get("new_subtitle")
    if not subtitle:
        subtitle = "please log in."
    form = LoginForm()
    if form.validate_on_submit():
        user = db_handler.check_email(form.data["email"])
        if user == None:
            return redirect(url_for("register", new_title="Unknown Email"))
        if not db_handler.check_password(user=user, password=form.data["password"]):
            return redirect(url_for("login", new_title="Wrong Password", new_subtitle="please try again"))
        login_user(user)
        return redirect(url_for("home", new_title="Log In Successful", new_subtitle="welcome back."))      
    return render_template("login.html", page="login", title=title, subtitle=subtitle, image_url=url_for('static', filename='images/banner-login.jpg'), form=form, logged_in=current_user.is_authenticated)

@app.route("/register", methods=["GET", "POST"])
def register():
    title = request.args.get("new_title", "")
    if not title:
        title = "Welcome to my Blog"
    form = RegisterForm()
    if form.validate_on_submit():
        # check if email already exists
        if db_handler.check_email(form.data["email"]):
            return redirect(url_for("login", new_title="User Already Registered"))
        with app.app_context():
            db_handler.register_user(form.data)
        # log in user
        user = db_handler.check_email(form.data["email"])
        login_user(user)
        return redirect(url_for("home", new_title="Successfully Registered", new_subtitle="welcome to my blog."))
    return render_template("register.html", page="register", title=title, subtitle="please register", image_url=url_for('static', filename='images/banner-register.jpg'), form=form, logged_in=current_user.is_authenticated)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home", new_title="Successfully logged out", new_subtitle="good bye"))

@app.route("/new-post", methods=["GET", "POST"])
def create_new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        print(form.data)
        with app.app_context():
            db_handler.create_new_post(form.data)
        return redirect(url_for("home", new_title="New Post Was Created", new_subtitle="thank you for posting."))
    if current_user.is_authenticated and current_user.id == 1:
        return render_template("new-post.html", title="Inspirtion", subtitle="is the art of finding magic in the ordenary" , image_url=url_for('static', filename='images/banner-new-post.jpg'), form=form, logged_in=current_user.is_authenticated)
    return redirect(url_for("home", new_title="Access not authorized", new_subtitle="please log in with admin account to write posts."))

@app.route("/post/<post_id>")
def show_post(post_id):
    post = db_handler.get_post_from_id(post_id)
    image_url = post.image_url
    if not image_url:
        image_url = "https://images.unsplash.com/photo-1499810631641-541e76d678a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3270&q=80"
    if current_user.is_authenticated:
        return render_template("post.html", title=post.title, subtitle=post.subtitle, image_url=image_url, post=post, logged_in=current_user.is_authenticated)
    return redirect(url_for("home", new_title="Access not authorized", new_subtitle="please log in or register to view posts."))


@app.route("/about")
def show_about():
    return render_template("about.html", page="about", title="About Me", subtitle="my own journey.", image_url=url_for('static', filename='images/banner-about.jpg'), logged_in=current_user.is_authenticated)


@app.route("/contact", methods=["GET", "POST"])
def show_contact():
    form = ContactForm()
    if form.validate_on_submit():
        eh = Email_Handler()
        eh.send_contact_mail(user_name=form.name.data,
                             user_mail_adress=form.email.data, user_message=form.message.data)
        return redirect(url_for("home", new_title="Mail Successfully Send", new_subtitle="i'll respond soon."))
    return render_template("contact.html", page="contact", title="Contact Me", subtitle="But be nice :)", image_url=url_for('static', filename='images/banner-contact.jpg'), form=form, logged_in=current_user.is_authenticated)