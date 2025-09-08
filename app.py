from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    item_list = ["python", "react", "node.js", "next.js", "websocket"]
    return render_template("index.html", items=item_list)

@app.route("/about")
def about():
    return "About Page"


@app.route("/user/<username>/<age>")
def show_user(username, age):
    return render_template("user.html", name=username, user_age=age)


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
