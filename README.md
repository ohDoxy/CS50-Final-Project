# Project BR

#### Video demo: 

#### Description
Project BR was created to make high school yearbook teams' job much easier. This idea was sparked by the yearbook advisor
at my school. She told me she wanted a program that emailed yearbook customers. In that email, they should be given the content
of the year book they ordered (i.e package, purchaser name, confirmation tag, etc.). When the student goes to pick up their yearbook,
the yearbook team can easily look at their name and know what package they bought.

## app.py
This file contains all of the flask implementation. Including sessions, routes, and database selection. All back end implementation
lives here. Logging in, registering and call of functions live here.

## helpers.py
This file contains all of helper functions used in app.py. The functions login_required and apology are influenced by CS50's 
functions. Apology notifies the user if they have done something wrong. The login_required function is a decorater that ensures
any route that is decorated by it, the user must be logged in.

The two most notable functions in helpers.py are "load" and "send_emails". The "load" function simply takes in a csv file as an 
argument, and loads it into an SQL database. This function is only capable of loading CSVs which is enforced by app.py's upload route.
Load uses csv.DictReader class to store it in a "rows" list. Then, rows is used to loop through the list of dicts and store them into
a "customers" table in SQL.

The "send_emails" function is called when the user clicks on the "Send Emails" button in uploaded.html. This functions retrives
all data in the customers table first. Then, for each row, it constructs an email with all neccessary information. To construct this,
this function uses the EmailMessage class in python. It sends an email containing the purchaser name, student name, student id,
package, amount paid, and confirmation tag.

## project.db
This file contains the database for the customers table. It contains a single table and is created when a file uses the load function

## website.db
This file contains a single SQL table "users". This table is used for registering users and logging them into the webiste.

## static/styles.css
This file is the style sheet for all gidgets in this web application. Most modifications are from the CS50's finance problem set.
The ones I have added are ".loader", "@keyframes spin", "#message", and "#follow-up". These are for the spinning loading image when
a file is being uploaded and the user is waiting.

## templates/apology.html
This file is from CS50's finance problem set. This template displays a message stating the users error.

## templates/index.html
This file contains the template for the home page of the web application. It simply retrives the first name of the user logged in
and welcomes them.

## templates/layout.html
This file contains the layout of all templates. It contains the navigation bar at the top of every route. It also contains multiple
buttons which point to different routes in app.py.

## templates/login.html
This file contains the login page html. It has a form which method is post. It prompts the user for a username and password.
It uses the login route in app.py to check if the user has entered the right credentials.

## templates/manage.html
This file contains a div and a form. The div is an alert message that says all emails are delivered. This route can only be accessed
if the user clicks "Send Emails" in uploaded.html. The form prompts the user to go back to index.html

## templates/register.html
This file is the registration form. It contains a single form which prompts a user for their first and last name, email, username,
and password they would like to sign up with. It uses a post request and inserts the information in an SQL database.

## templates/upload.html
This file contains JavaScript and a form. The form has a user select a file restricted to .csv. However, app.py enforces the file can
only be .csv even if the html is changed by an adversary. It uses a post request. When the form is submitted, a function called "func"
is called within the script. This function shows all of the css I have added which is the loading image.

## templates/uploaded.html
This file also contains JavaScript and a form. The form has two options, "Change File" and "Send Emails". The change file option
simply returns the user to the select file form. The send emails options uses the send_emails function in helpers to send emails
to all yearbook customers. The script does the same thing as in upload.html.