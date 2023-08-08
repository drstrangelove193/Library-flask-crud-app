from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import login_required, warning

app = Flask(__name__)
app.secret_key = 'secret_key'


#Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Configure database using cs50 package
db = SQL("sqlite:///library.db")


@app.after_request
def after_request(response):
    # Ensure that responses are not cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route('/')
@login_required
def index():
    """We are displaying the books of logged in user"""
    user = db.execute("SELECT * FROM users WHERE id=?", session["user_id"])
    users_books = db.execute(
        "SELECT * FROM books WHERE user_id=?", session["user_id"]
    )
    return render_template('index.html', book_shelf=users_books, user=user)


'''
This route is to delete a book that we click on, we keep track of it by book_id , that is unique
'''
@app.route('/delete/<int:book_id>')
def delete(book_id):
    db.execute(
        "DELETE FROM books WHERE book_id=?", book_id)
    return redirect("/")

'''
Again we keep track of books by unique book_id
'''
@app.route('/update/<int:book_id>', methods=["GET", "POST"])
def update_book(book_id):
    book = db.execute(
        "SELECT * FROM books WHERE book_id=?", book_id)

    # Now it is almost same as inserting a new book into database just now we have to update it.
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        shelves = request.form.get("shelves")

        # Check for inputs and validate
        if not title:
            return warning("Must Enter a Title!")
        if not author:
            return warning("Must Enter an Author!")
        if not genre:
            return warning("Must Specify a Genre of a Book!")
        if not rating:
            return warning("Must Rate a Book!")
        if not shelves:
            return warning("Let us know if you've read a book or not!")

        # converting string to float 
        rating = float(rating)

        # Inserting an updated date and time
        current_datetime = datetime.now()

        # Updating a book into books library
        db.execute(
            "UPDATE books SET title=?, author=?, genre=?, rating=?, shelves=?, curr_date=? WHERE book_id=?",
            title, author, genre, rating, shelves, current_datetime, book_id)

        # Display the message that Book was successfully updated
        flash("The Book was successfully updated!")
        return redirect("/")
    else:
        # It is a default method, so we should display the form for user to Update
        return render_template("update.html", book=book)    





@app.route('/addbook', methods=["GET", "POST"])
def add_book():
    # If user submitted a Form 
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        shelves = request.form.get("shelves")

        # Check for inputs and validate
        if not title:
            return warning("Must Enter a Title!")
        if not author:
            return warning("Must Enter an Author!")
        if not genre:
            return warning("Must Specify a Genre of a Book!")
        if not rating:
            return warning("Must Rate a Book!")
        if not shelves:
            return warning("Let us know if you've read a book or not!")

        # converting string to float 
        rating = float(rating)

        # Inserting A new book into books library
        db.execute(
            "INSERT INTO books (user_id, title, author, genre, rating, shelves) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], title, author, genre, rating, shelves)

        # Display the message that Book was successfully added to library
        flash("The Book was successfully added to Library")
        return redirect("/")

    else:
        # default method get, display the form to add the book
        return render_template("addbook.html")




@app.route('/login', methods=["GET", "POST"])
def login():
    # First Clear the session
    session.clear()

    #If user submits the form, i.e method="POST"
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        
        # We should validate fields for empty username and password
        if not username or not password :
            return warning("Please Provide Credentials")
        
        # Get username from database
        info = db.execute(
            "SELECT * FROM users WHERE username=?", username)
        
        #We must make sure that user exists and password is correct
        if len(info) != 1 or not check_password_hash(info[0]["password"], password):
            return warning("Invalid Username and/or Password")

        # Remember Logged In user
        session["user_id"] = info[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # The Method is Get , so we show default login for to User
    else:
      return render_template('login.html')



@app.route('/logout')
def logout():
    
    # Clear Session , forget user id
    session.clear()

    # redirect user to login
    return redirect("/")


@app.route('/register', methods=["GET", "POST"])
def register():
    # If user submits form via POST we must save values
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if user already exists in our users database
        exists = db.execute(
            "SELECT * FROM users WHERE username=?", username)

        # Now must do some checks for inputs
        if not username or not password or not confirmation:
            return warning("Can't leave these fields empty!")
        elif not password == confirmation:
            return warning("Password and Confirmation do not match!")
        elif len(exists):
            return warning("User Already exists in database!")
        else:
            # In this case we got a new user and we will store his/hers information, we will hash the password and save it like that
            hash = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?);",
                username, hash)
            row = db.execute("SELECT id FROM users WHERE username =?", username)
            session["user_id"] = row[0]["id"]
        return redirect("/")
    else:
        return render_template("register.html")



if __name__ == "__main__":
    app.run(debug=True)
