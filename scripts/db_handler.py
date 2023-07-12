from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import bleach
from datetime import date

db = SQLAlchemy()

# strips invalid tags/attributes
def strip_invalid_html(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']

    allowed_attrs = {
        'a': ['href', 'target', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
    }

    cleaned = bleach.clean(content,
                           tags=allowed_tags,
                           attributes=allowed_attrs,
                           strip=True)

    return cleaned


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    posts = db.relationship("BlogPost", back_populates="author")
    comments = db.relationship("Comment", back_populates="comment_author")

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.relationship("User", back_populates="posts")
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(250), nullable=False)
    comments = db.relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = db.relationship("User", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = db.relationship("BlogPost", back_populates="comments")

class Db_Handler():
    def __init__(self):
        pass
    
    def register_user(self, data):
        new_user = User(username=data["username"], email=data["email"], password=generate_password_hash(password=data["password"], method="sha256", salt_length=8))
        db.session.add(new_user)
        db.session.commit()

    def create_new_post(self, data, author_id):
        author_id = author_id
        title = data["title"]
        subtitle = data["subtitle"]
        image_url = data["image_url"]
        body = strip_invalid_html(data["body"])
        current_date = date.today().strftime("%x")
        new_post = BlogPost(title=title, subtitle=subtitle, image_url=image_url, body=body, date=current_date, author_id=author_id)
        db.session.add(new_post)
        db.session.commit()

    def edit_post(self, data, post_id):
        post = self.get_post_from_id(post_id)
        post.title = data["title"]
        post.subtitle = data["subtitle"]
        post.image_url = data["image_url"]
        post.body = data["body"]
        post.date = date.today().strftime("%x")
        db.session.commit()

    def get_all_posts(self):
        posts = BlogPost.query.all()
        return posts
    
    def get_post_from_id(self, id):
        post = BlogPost.query.get(id)
        return post
  
    def get_user_from_id(self, id):
        user = User.query.get(id)
        return user
    
    def check_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user

    def check_password(self, user, password):
        return check_password_hash(pwhash=user.password, password=password)
    
    def delete_post(self, post_id):
        post = self.get_post_from_id(post_id)
        db.session.delete(post)
        db.session.commit()