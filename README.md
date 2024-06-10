# Sunrise Learning Center Library
## Introduction
This web application allows its users (librarians) to manage library functions such as adding and removing books and members, issuing and returning books, and managing some other aspects of an organization.

<br>

## Technologies used
- HTML  
- CSS  
- JavaScript (jQuery)  
- Ajax 
- Python (Flask)  
- Jinja
- PostgreSQL

<br>

## Quick start guide
Install packages from a requirements file, preferably in your active virtual environment, by navigating to the project directory and typing the following command in your command prompt or terminal:
```bash 
pip install -r requirements.txt
``` 
and then run a command 
```bash
flask run
```
```bash
gunicorn app:app
```
Once started, please use username: **admin** and password: **00000** to log in as an administrator and gain access to all available features of an LMS. Regular users (librarians) would have limited access to some options.

Wherever in the app, you can access any of the following sections: manage members, add a member, edit members' details (Although, I could not solve the problem to show changes) catalogue of books, manage books, add a new book, checkout, book returns, Library Management (or account if logged in as librarian), FAQ and logout. with '/account' it will redirect you to change and set new password to current account. 

<br>

## Description

Static folder contains a book.jpeg used as a background image for an app. There are couple of .css files: style.css as a general one, while others like popups.css, mamagement.css and offcanvas.css define a style only for specific parts or features of an app. Color scheme persists throughout the application. Script.js contains all JavaScript (jQuery) used:

- ***functions that trigger and populate popups*** on members and books templates. Once the Edit button is selected for a particular book or member, a pop-up window appears. It contains all the details of the book or member in question and allow users to modify them.

- ***dynamic search*** is implemented on members, books, catalogue and index (book returns) templates. For example, users can search for a book by its title, author name or ID. I mostly used JSON responses from the server to dynamically populate tables on the keyup event. Exceptions are index and transaction history page where information already displayed on templates is used with jQuery to hide or show table rows based on user query. I simply wanted to try different approaches.

- ***books checkout process*** is carried out completely with JavaScript, until submission when server takes over. I didn't want to interrupt checkout process, which involves multiple steps, with page reloads or redirects. Checkout section requires a user to enter a member's id in order to initiate the checkout process. I assumed that every member would bring their member's card with them. After member id is entered, member details will show below as well as a field that shows how many books the member has already borrowed and not returned yet (if any). Book search field is now visible and a book can be searched for by its id. Book details will appear and the user can add that book to the basket or cancel it. If a book has zero availability, the same book has already been added to the basket or if a member already has the same copy of a book checked out previously, user won't be allowed to add that book to the basket. Users can add multiple books and remove them from the basket. Once finished with adding books, checkout button can be selected and user will be redirected back to the Book Returns section (index template) and message will display for successful checkout.

- ***book returns off-canvas related script*** allows users to click on a specific member (row) which then triggers and populates off-canvas with books checked out to that member. Options to return single or all books at once are available here. However, I was unable to achieve this objective as I didn't have enough time to figure out the problem. 

- ***transactions history filters*** enable users to filter out transactions by type, librarian who made them, book id, member id, and sort them ASC or DESC by time of transaction. Filters, if combined, work well with each other.

Templates directory includes all the html templates used. At the very beginning, the register template was accessible from the login template. But I realized this would be a poor design decision as any user would be able to register new librarians. Link to Library Management, which now has an option to register new librarian, is accessible only to the user logged-in in as an administrator.

App.py contains all of the python code, along with configuration part, imports, and all routes.

Library.sql has four tables: books, members, transactions and staff. Database is populated with 20 actual books and their details together with 20 random names and details of members. There has been a great deal of change over time. I have implemented a soft delete technique for all deletions in the application that tags removed entries as deleted and then I filtered those out from relevant templates.

- *** Link to Render.com ***
  https://sunrise-learning-center-library.onrender.com
- *** Link to GitHub Repo ***
  https://github.com/Dylanjb96/Sunrise-Learning-Center-Library
  
  
