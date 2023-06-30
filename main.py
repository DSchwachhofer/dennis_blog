from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

from scripts.forms import ContactForm, LoginForm, RegisterForm
from scripts.email import Email_Handler
from scripts.db_handler import db, Db_Handler

from datetime import date
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()



app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db.init_app(app)

# creating database
# with app.app_context():
#     db.create_all()


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

    return render_template("index.html", page="home", title=title, subtitle=subtitle, image_url=url_for('static', filename='images/banner-home.jpg'))

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for("home", new_title="Log In Successful", new_subtitle="welcome back."))
    return render_template("login.html", page="login", title="Welcome Back", subtitle="please log in", image_url=url_for('static', filename='images/banner-login.jpg'), form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for("home", new_title="Successfully Registered", new_subtitle="welcome to my blog."))
    return render_template("register.html", page="register", title="Welcome to my Blog", subtitle="please register", image_url=url_for('static', filename='images/banner-register.jpg'), form=form)


@app.route("/post<post_id>")
def show_post(post_id):
    return render_template("post.html", title="The Art of Minimalism", subtitle="Discover the Beauty of Simplicity", image_url="https://images.unsplash.com/photo-1449247709967-d4461a6a6103?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3271&q=80")


@app.route("/about")
def show_about():
    return render_template("about.html", page="about", title="About Me", subtitle="my own journey.", image_url=url_for('static', filename='images/banner-about.jpg'))


@app.route("/contact", methods=["GET", "POST"])
def show_contact():
    form = ContactForm()
    if form.validate_on_submit():
        eh = Email_Handler()
        eh.send_contact_mail(user_name=form.name.data,
                             user_mail_adress=form.email.data, user_message=form.message.data)
        return redirect(url_for("home", new_title="Mail Successfully Send", new_subtitle="i'll respond soon."))
    return render_template("contact.html", page="contact", title="Contact Me", subtitle="But be nice :)", image_url=url_for('static', filename='images/banner-contact.jpg'), form=form)
