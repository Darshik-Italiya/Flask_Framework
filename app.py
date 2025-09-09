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
        name = request.form.get("name")
        age = request.form.get("age")
        return f"Data Submitted Successfully.. name: {name}, age: {age}"
    else:
        name = request.args.get("name")
        age = request.args.get("age")
        return f"Data Submitted Successfully.. name: {name}, age: {age}"


if __name__ == "__main":
    app.run(debug=True)
