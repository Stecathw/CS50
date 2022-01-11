import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session


# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = os.urandom(16)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        if not name or month == '' or day == '':
            flash('Please, enter a valid name, month and day !', category='error')
            return redirect("/")
        else:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)"
            , name, month, day)
            flash('Birthday added succesfully!', category='success')
            return redirect("/")
    else:
        # TODO: Display the entries in the database on index.html
        rows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", rows = rows)
        

@app.route("/delete/<int:id>")
def delete(id):
    birthday_to_delete = db.execute("DELETE FROM birthdays WHERE id=?", id)
    flash('Birthday correctly deleted', category='correct')
    return redirect("/")