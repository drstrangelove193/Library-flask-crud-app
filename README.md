# Library of Giorgi

#### Description:
This is a mini-project, a library in which user can store his/hers favorite books. Basically, a new user who enters the Library
at first must register and sign in then he/she can add his/hers favorite books intro the database. I used Python/Flask, HTML, CSS
SQLite3.

I designed 2 tables in the database.First named users to store unique user_id-s and keep track of users using sessions.
Second table is called books, in books table there are following columns: 
book_id - to keep track of books,
user_id - to connect to users table,
title - for book title,
author - book author,
genre - book genre,
rating - float point number from 0 including 5
shelves - with 2 options "To-read" and "read"
curr_date - to keep track of date when the book is added and when the book is updated

After user logs in, then user can Add a book. then user can update it or delete it from the database.
I re-used some of the code from a Pset9 - Finance for login/logout register and helper functions
In Helpers.py There are 2 functions , first:warning - that displays the warning message to user, when something is not working out
another: decorated function to request user to login

There I use custom books icon to return to index page every time user clicks it.
I created couple of html files to match with routes, all of them extends layout.html
in Layout.html I use navbar in the header and ul - for add book, login/ log out and register, in the end of layout.html 
there is "main" tag and all the other pages content goes in there.

To Display data from database I use Bootstrap Table, using bootstrap for styling and also using main.css file where I have plain CSS.
for update and delete buttons, for background of body , logo etc...

In the end I want to say that , as a begginer in Computer Science This project was really a challenge for me and I am glad I did it. I want to thank all the CS50 Staff and Harvard University for this amazing opportunity!
