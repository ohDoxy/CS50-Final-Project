""" HELPER FUNCTIONS FOR MAIN """

import csv
from cs50 import SQL

# Create SQL connection
open("sales.db", "w").close()
db = SQL("sqlite:///sales.db")

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
CREATE TABLE users (
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
    db.execute("CREATE INDEX id ON users (student_id)")
    db.execute("CREATE INDEX package ON users (package)")
    db.execute("CREATE INDEX purchaser_name ON users (purchaser_name)")
    db.execute("CREATE INDEX purchaser_email ON users (purchaser_email)")
    
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
        
        db.execute("""INSERT INTO users (student_id, first_name, last_name, confirmation, package, paid, purchaser_name,
                   purchaser_email, sale_date)
                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", id, first_name, last_name, confirmation, package, paid, purchaser_name,
                   purchaser_email, sale_date)
