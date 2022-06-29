""" HELPER FUNCTIONS FOR MAIN """

import os
import csv
import qrcode
import smtplib
import imghdr

from cs50 import SQL
from flask import redirect, session, render_template
from functools import wraps
from email.message import EmailMessage

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("EMAIL_PASS")

# Create SQL connection
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
        
    db.execute("DROP TABLE IF EXISTS customers")
    
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
                sale_date TEXT NOT NULL, 
                qr_code TEXT      
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
        id = row.get("Student Id", "NULL").strip()
        first_name = row.get("First Name", "NULL").strip()
        last_name = row.get("Last Name", "NULL").strip()
        confirmation = row.get("Confirmation", "NULL").strip()
        package = row.get("Display Name", "NULL").strip()
        paid = row.get("Amount Paid", "NULL").strip()
        purchaser_name = row.get("Purchaser Name", "NULL").strip()
        purchaser_email = row.get("Purchaser Email", "NULL").strip()
        sale_date = row.get("Sale Date", "NULL").strip()
        
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


def send_emails():
    """ Send emails of information """
    
    # SQL Query for database
    rows = db.execute("SELECT * FROM customers")
    
    for row in rows:
        
        # Setup list of recievers (purchaser and student)
        purchaser_email = row["purchaser_email"]
        student_id = row["student_id"]
        student_email = f"{student_id}@lcps.org"
        recievers = [purchaser_email, student_email]
        
        # Setup email connection
        msg = EmailMessage()
        msg["Subject"] = "Purchased Yearbook Information"
        msg["From"] = EMAIL
        msg["To"] = recievers
        
        # Construct message
        msg.set_content(f"""Dear yearbook purchaser,
                        
Below is the information of the yearbook you have purhcased. Please show this email when you pick up your yearbook.
                        
Purchaser Name (Last, First): {row["purchaser_name"]}
Student Name: {row["first_name"]} {row["last_name"]}
Student ID: {row["student_id"]}
Package: {row["package"]}
Amount Paid: {row["paid"]}
Confirmation Tag: {row["confirmation"]}
                        
Thank you for purchasing a yearbook!""")
        
        # Send message
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            
            smtp.login(EMAIL, PASSWORD)
            
            smtp.send_message(msg)
        
        print("sent")