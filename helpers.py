""" HELPER FUNCTIONS FOR MAIN """
import os

import csv
from cs50 import SQL
from flask import redirect, session, render_template
from functools import wraps

# Create SQL connection
open("project.db", "w").close()
db = SQL("sqlite:///project.db")

def load(filename):
    """ LOAD CSV FILE INTO DATABASE """
    
    # Read csv file into a list
    rows = []
    with open(filename, 'r') as file:
        
        # Read each row as a dictionary
        reader = csv.DictReader(file)
        for row in reader:
            
            rows.append(row)
        
        file.close()
    
    # Create table
    db.execute("""
CREATE TABLE customers (
                student_id TEXT,
                first_name TEXT,     
                last_name TEXT,      
                confirmation TEXT,   
                package TEXT NOT NULL,        
                paid TEXT NOT NULL,        
                purchaser_name TEXT NOT NULL, 
                purchaser_email TEXT NOT NULL,
                sale_date TEXT NOT NULL       
        )
               """)
    db.execute("CREATE INDEX id ON customers (student_id)")
    db.execute("CREATE INDEX package ON customers (package)")
    db.execute("CREATE INDEX purchaser_name ON customers (purchaser_name)")
    db.execute("CREATE INDEX purchaser_email ON customers (purchaser_email)")
    
    # Pop headers out of dict
    rows.pop(0)
    
    # Store data in SQL table
    for row in rows:
        
        # Initialize variables
        id = row["Student Id"].strip()
        first_name = row["First Name"].strip()
        last_name = row["Last Name"].strip()
        confirmation = row["Confirmation"].strip()
        package = row["Display Name"].strip()
        paid = row["Amount Paid"].strip()
        purchaser_name = row["Purchaser Name"].strip()
        purchaser_email = row["Purchaser Email"].strip()
        sale_date = row["Sale Date"].strip()
        
        db.execute("""INSERT INTO customers (student_id, first_name, last_name, confirmation, package, paid, purchaser_name,
                   purchaser_email, sale_date)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", id, first_name, last_name, confirmation, package, paid, purchaser_name,
                   purchaser_email, sale_date)



def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code