from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from forms import ContactForm

from datetime import date
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
Bootstrap(app)


# add a current year variable which will be accessed from all sites.
@app.context_processor
def inject_current_year():
    return {"current_year": date.today().year}


@app.route("/")
def home():
    return render_template("index.html", page="home", title="Dennis's Blog", subtitle="A collection of random musings.", image_url=url_for('static', filename='images/banner-home.jpg'))


@app.route("/post<post_id>")
def show_post(post_id):
    return render_template("post.html", title="The Art of Minimalism", subtitle="Discover the Beauty of Simplicity", image_url="https://images.unsplash.com/photo-1449247709967-d4461a6a6103?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3271&q=80")


@app.route("/about")
def show_about():
    return render_template("about.html", page="about", title="About Me", subtitle="My own journey.", image_url=url_for('static', filename='images/banner-about.jpg'))


@app.route("/contact", methods=["GET", "POST"])
def show_contact():
    form = ContactForm()
    if form.validate_on_submit():
        print("SENDING MAIL")
        # return "SUCCESS"
    return render_template("contact.html", page="contact", title="Contact Me", subtitle="But be nice :)", image_url=url_for('static', filename='images/banner-contact.jpg'), form=form)
