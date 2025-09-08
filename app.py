from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Home Page"


@app.route("/about")
def about():
    return "About Page"


@app.route("/user/<username>/<age>")
def show_user(username, age):
    return "User %s, %s" % (username, age)


@app.route("/post/<int:post_id>", methods=["GET"])
def show_post(post_id):
    return "Post_ID: %s" % post_id


@app.route("/submit", methods=["GET", "POST"])
def submitData():
    if request.method == "POST":
        return "Data Submitted Successfully.."
    else:
        return "Please Submit the form!"


if __name__ == "__main":
    app.run(debug=True)
