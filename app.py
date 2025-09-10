from flask import Flask, request, render_template, redirect, url_for, flash
from form import MyForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["SECRET_KEY"] = "rk4hi5jthn5tji56h6kj7nkjntjgkfng"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static", "images")
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}


db = SQLAlchemy(app)


# User Table
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"User: {self.name}, email: {self.email}"


# Blog Table
class Blog(db.Model):
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    image_file = db.Column(db.String(200), default="default.jpg")
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"Blogs: {self.title}, {self.content}, {self.created_at}"


@app.route("/")
def home():
    item_list = ["python", "react", "node.js", "next.js", "websocket"]
    return render_template("index.html", items=item_list)


@app.route("/users")
def users():
    users = User.query.all()
    form = MyForm(obj=users)
    return render_template("users/index.html", users=users, form=form)


@app.route("/new-user", methods=["GET", "POST"])
def new_user():
    form = MyForm()
    if form.validate_on_submit():

        new_user = User(name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Form submitted successfully...")

        return redirect(url_for("users"))
    else:
        return render_template("/users/create.html", form=form)


@app.route("/users/<int:id>/edit", methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get(id)
    form = MyForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        flash("User updated successfully")
        return redirect(url_for("users"))

    return render_template("users/edit.html", form=form, user=user)


@app.route("/users/<int:id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully...")
    return redirect(url_for("users"))


@app.route("/submit", methods=["GET", "POST"])
def submitData():
    form = MyForm()
    if form.validate_on_submit():

        new_user = User(name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Form submitted successfully...")

        return redirect(url_for("submitData"))
    else:
        return render_template("form.html", form=form)


@app.route("/users/<int:id>")
def show_user(id):
    user = User.query.get(id)
    return render_template("users/show.html", user=user)


@app.route("/blogs")
def blogs():
    blogs = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template("blogs/index.html", blogs=blogs)


def allowed_files(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/blog/new", methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        file = request.files.get("image_file")
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = "default.jpg"

        # Store relative path for image_file
        image_path = os.path.join("images", filename)

        new_blog = Blog(title=title, content=content, image_file=image_path)

        db.session.add(new_blog)
        db.session.commit()

        return redirect(url_for("blogs"))

    return render_template("blogs/create.html")


with app.app_context():
    db.create_all()

if __name__ == "__main":
    app.run(debug=True)
