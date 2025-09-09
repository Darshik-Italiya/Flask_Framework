from flask import Flask, request, render_template, redirect, url_for, flash
from form import MyForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "rk4hi5jthn5tji56h6kj7nkjntjgkfng"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"User: {self.name}, email: {self.email}"


@app.route("/")
def home():
    item_list = ["python", "react", "node.js", "next.js", "websocket"]
    return render_template("index.html", items=item_list)


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users/index.html", users=users)


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


if __name__ == "__main":
    app.run(debug=True)
