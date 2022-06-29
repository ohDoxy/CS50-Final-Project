import os
from re import A

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from requests import Response
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import load, login_required, apology

# Conifgure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQL database
db = SQL("sqlite:///website.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """ Welcome user """
    
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    first_name = rows[0]["first_name"]
    
    return render_template("index.html", first_name=first_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must enter username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must enter password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("username or password is incorrect")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
    
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Check to see if user accesses by form
    if request.method == "POST":
        # Initialize all field values
        first_name = request.form.get("first-name")
        last_name = request.form.get("last-name")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Check for vacant fields
        if not first_name:
            return apology("must provide first name")
        
        if not last_name:
            return apology("must provide last name")
        
        if not email:
            return apology("must provide email")

        # Check if there is a username and password
        if not username or not password:
            return apology("must enter a username and password")

        # Check to see if confirmation password match
        if password != confirmation:
            return apology("passwords do not match")
        
        # Check to see if email is already used
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        if len(rows) != 0:
            return apology("email already in use")

        # Check to see if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        # If there are no rows, username is available
        if len(rows) != 0:
            return apology("username already taken")

        # Hash the password and insert data into database
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (first_name, last_name, email, username, hash) VALUES(?, ?, ?, ?, ?)", 
                   first_name, last_name, email, username, hash)

        return redirect("/")

    # If get, return the template
    return render_template("register.html")



@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """ Accept a CSV file and upload data """
    
    if request.method == "POST":
        
        file = request.form.get("file")
        
        # Check if a file was submitted
        if not file:
            return apology("must include file")
        
        # See if type of file is csv
        pos_of_dot = file.find('.')
        filetype = file[pos_of_dot+1:]
        
        if filetype.lower() != "csv":
            return apology("file must be csv")
        
        # Load file
        load(file)
        
        return render_template("uploaded.html", file=file)
    
    return render_template("upload.html")