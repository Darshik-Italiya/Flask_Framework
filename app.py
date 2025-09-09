from flask import Flask, request, render_template, redirect, url_for, flash
from form import MyForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "rk4hi5jthn5tji56h6kj7nkjntjgkfng"

@app.route("/")
def home():
    item_list = ["python", "react", "node.js", "next.js", "websocket"]
    return render_template("index.html", items=item_list)

@app.route("/submit", methods=["GET", "POST"])
def submitData():
    form = MyForm()
    if form.validate_on_submit():
        flash("Form submitted successfully...")
        
        return redirect(url_for("submitData"))
    else:
       return render_template("form.html", form=form)


if __name__ == "__main":
    app.run(debug=True)
