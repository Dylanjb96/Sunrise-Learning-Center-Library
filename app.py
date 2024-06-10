from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask, redirect, render_template, request, session, flash, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from model import db, Staff
from flask_login import login_required
import logging




# Configure application
app = Flask(__name__)


# Configure session to use filesystem, not cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://library_pcou_user:iceO5VPJeaWZvrgGojbHQtvoR9x5ZySL@dpg-cpavtvv79t8c73b62bh0-a.frankfurt-postgres.render.com/library_pcou'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



# Ensure responses are not cached for privacy reasons
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Login required decorator, url: https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


GENRES = ['Art', 'Autobiography', 'Biography', 'Business', 'Children', 'Comics', 'Cookbooks', 'Drama', 'Fantasy', 'Fiction', 'Graphic Novel', 'Historical Fiction', 'History', 'Horror', 'Humor', 'Memoir', 'Music', 'Mystery', 'Non-fiction', 'Other', 'Poetry', 'Psychology', 'Romance', 'Science', 'Science Fiction', 'Self-help', 'Spiritual/Religious', 'Sports', 'Thriller', 'Travel']


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''Librarian login'''

    # Clear any user_id
    session.clear()

    # User reached route via GET
    if request.method == 'GET':
        return render_template('login.html')
    
    # User reached route via POST
    else:
        # Ensure username and password are submitted
        if not request.form.get('username') or not request.form.get('password'):
            flash('Username and password fields are required!')
            return render_template('login.html')
        
        # Query database for username
        query = text('SELECT * FROM staff WHERE username = :username AND deleted = :deleted')
        user = db.session.execute(query, {'username': request.form.get('username'), 'deleted': 0}).fetchone()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user[3], request.form.get('password')):
            flash('Incorrect username and/or password!')
            return render_template('login.html')
        
        # Remember user that has logged in
        session['user_id'] = user[0]

        # Redirect user to a home page
        return redirect('/')
    

@app.route('/logout')
def logout():
    '''Librarian logout'''
    
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect('/login')


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    '''Index page: show list of currently issued books. Return functionality'''

    # Get user_id from session
    user_id = session['user_id']
    logging.debug(f'user_id: {user_id}')

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :id'), {'id': user_id}).fetchone()[0]
    logging.debug(f'Librarian name: {name}')
    
    # Query database for transactions, books & members
    transactions = db.session.execute(text('SELECT * FROM transactions WHERE type = :type'), {'type': 'borrow'}).fetchall()
    members = db.session.execute(text('SELECT * FROM members JOIN transactions ON members.member_id = transactions.borrower_id WHERE type = :type GROUP BY members.member_id, members.name, transactions.borrower_id, transactions.book_id, transactions.type, transactions.employee_id, transactions.time ORDER BY transactions.time ASC'), {'type': 'borrow'}).fetchall()
    books = db.session.execute(text('SELECT * FROM books')).fetchall()

    # Convert CursorResult to a list of dictionaries
    transactions_list = [dict(row._mapping) for row in transactions]
    members_list = [dict(row._mapping) for row in members]
    books_list = [dict(row._mapping) for row in books]

    logging.debug(f'Transactions: {transactions_list}')
    logging.debug(f'Members: {members_list}')
    logging.debug(f'Books: {books_list}')

    # User reached route via GET
    if request.method == 'GET':
        member_due = []

        # Iterate over members dict
        for member in members_list:
            # Append member to the member_due list if one has any number of borrowed books
            if member['borrowed'] > 0:
                member_due.append(member)

        logging.debug(f'Members due for return: {member_due}')

        # Render index.html
        return render_template('index.html', name=name, members=member_due, books=books_list)

    # User reached route via POST
    else:
        # Check request header and send whole list of books and transactions as json response
        if request.headers['Content-Type'] == 'application/x-www-form-urlencoded; charset=UTF-8':
            return jsonify(books=books_list, transactions=transactions_list)
        
        # User selection
        book_id = request.form.get('id')
        book_ids = request.form.getlist('all_ids')
        member_id = request.form.get('memberId')

        logging.debug(f'book_id: {book_id}, book_ids: {book_ids}, member_id: {member_id}')

        if book_id:
            # Query database for number of books borrowed by a particular member
            borrowed = db.session.execute(text('SELECT borrowed FROM members WHERE member_id = :id'), {'id': member_id}).fetchone()[0]
            logging.debug(f'Borrowed books by member {member_id}: {borrowed}')

            # Query database for book availability
            available = db.session.execute(text('SELECT available FROM books WHERE id = :id'), {'id': book_id}).fetchone()[0]
            logging.debug(f'Book {book_id} availability: {available}')

            # Update transaction type from borrow to borrowed
            db.session.execute(text('UPDATE transactions SET type = :type WHERE borrower_id = :borrower_id AND book_id = :book_id'), {'type': 'borrowed', 'borrower_id': member_id, 'book_id': book_id})

            # Insert new data into transactions table
            db.session.execute(text('INSERT INTO transactions (borrower_id, book_id, type, employee_id) VALUES (:borrower_id, :book_id, :type, :employee_id)'), {'borrower_id': member_id, 'book_id': book_id, 'type': 'returned', 'employee_id': user_id})

            # Update book availability
            db.session.execute(text('UPDATE books SET available = :available WHERE id = :id'), {'available': available + 1, 'id': book_id})

            # Update number of books borrowed by a member
            db.session.execute(text('UPDATE members SET borrowed = :borrowed WHERE member_id = :id'), {'borrowed': borrowed - 1, 'id': member_id})

            flash('Book returned')
            
            return redirect('/')
        
        if book_ids:
            # Iterate over list of book ids
            for book_id in book_ids:
                # Query database for number of books borrowed by a particular member
                borrowed = db.session.execute(text('SELECT borrowed FROM members WHERE member_id = :id'), {'id': member_id}).fetchone()[0]
                logging.debug(f'Borrowed books by member {member_id}: {borrowed}')

                # Query database for book availability
                available = db.session.execute(text('SELECT available FROM books WHERE id = :id'), {'id': book_id}).fetchone()[0]
                logging.debug(f'Book {book_id} availability: {available}')

                # Update transaction type from borrow to borrowed
                db.session.execute(text('UPDATE transactions SET type = :type WHERE borrower_id = :borrower_id AND book_id = :book_id'), {'type': 'borrowed', 'borrower_id': member_id, 'book_id': book_id})

                # Insert new data into transactions table
                db.session.execute(text('INSERT INTO transactions (borrower_id, book_id, type, employee_id) VALUES (:borrower_id, :book_id, :type, :employee_id)'), {'borrower_id': member_id, 'book_id': book_id, 'type': 'returned', 'employee_id': user_id})

                # Update book availability
                db.session.execute(text('UPDATE books SET available = :available WHERE id = :id'), {'available': available + 1, 'id': book_id})

                # Update number of books borrowed by a member
                db.session.execute(text('UPDATE members SET borrowed = :borrowed WHERE member_id = :id'), {'borrowed': borrowed - 1, 'id': member_id})

            flash('All books returned')
            
            return redirect('/')

        # If no book_id or book_ids are provided
        flash('No book selected for return')
        return redirect('/')




@app.route('/catalogue')
@login_required
def catalogue():
    '''Books sorted alphabetically by title, author or genre. Current stock and search books feature'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()[0]

    # Sort by title
    if request.args.get('sort') == 'title':
        
        # Redirect to catalogue route - default is sorted by title
        return redirect('/catalogue')
    
    # Sort by author
    elif request.args.get('sort') == 'author':
        
        # Query database for books and sort by author
        books = db.session.execute(text('SELECT * FROM books WHERE deleted = :deleted ORDER BY author ASC'), {'deleted': 0}).fetchall()
        return render_template('catalogue.html', books=books, name=name)
    
    # Sort by genre
    elif request.args.get('sort') == 'genre':
        
        # Query database for books and sort by genre
        books = db.session.execute(text('SELECT * FROM books WHERE deleted = :deleted ORDER BY genre ASC'), {'deleted': 0}).fetchall()
        return render_template('catalogue.html', books=books, name=name)
    
    # User reached route from navbar - query database for books and sort by title
    books = db.session.execute(text('SELECT * FROM books WHERE deleted = :deleted ORDER BY title ASC'), {'deleted': 0}).fetchall()
    return render_template('catalogue.html', books=books, name=name)


@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    '''Books management'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()[0]

    # User reached route via GET
    if request.method == 'GET':
        # Query database for books and sort by title
        books_result = db.session.execute(text('SELECT * FROM books WHERE deleted = :deleted ORDER BY title ASC'), {'deleted': 0}).fetchall()

        # Convert result to list of dictionaries
        books = []
        for row in books_result:
            books.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'genre': row[3],
                'year': row[4],
                'stock': row[5],
                'available': row[6]
            })

        # Search books query and selected field
        query = request.args.get('query')
        field = request.args.get('field')

        # Query exists and search by field is 'id', return exact match as JSON response
        if query and field == 'id':
            match = db.session.execute(text('SELECT * FROM books WHERE deleted = :deleted AND id = :id'), {'deleted': 0, 'id': query}).fetchone()
            if match:
                match_dict = {
                    'id': match[0],
                    'title': match[1],
                    'author': match[2],
                    'genre': match[3],
                    'year': match[4],
                    'stock': match[5],
                    'available': match[6]
                }
                return jsonify(match_dict)
            else:
                return jsonify({})

        # Any other search field selected
        elif query and field in ['title', 'author', 'genre', 'year']:
            matches = [book for book in books if query.lower() in str(book[field]).lower()]
            return jsonify(matches)

        # Render books template
        return render_template('books.html', books=books, name=name, genres=GENRES)

    # User reached route via POST
    else:
        # Get the value of the button user clicked on
        button = request.form.get('button')

        # Remove button selected
        if button == 'remove':
            # Query database for the title of the book to be removed
            removed = db.session.execute(text('SELECT title FROM books WHERE id = :id'), {'id': request.form.get('id')}).fetchone()[0]

            # Delete book (tag as deleted)
            db.session.execute(text('UPDATE books SET deleted = :deleted WHERE id = :id'), {'deleted': 1, 'id': request.form.get('id')})
            db.session.commit()

            # Flash book removed message
            flash(f'Book "{removed}" has been successfully removed!')

            # Redirect to books route with updated table
            return redirect('/books')

        # Update button selected on popup form
        elif button == 'update':
            # User input
            id = request.form.get('form_id')
            title = request.form.get('title')
            author = request.form.get('author')
            genre = request.form.get('genre')
            year = request.form.get('year')
            current_stock = db.session.execute(text('SELECT stock FROM books WHERE id = :id'), {'id': id}).fetchone()[0]
            available = db.session.execute(text('SELECT available FROM books WHERE id = :id'), {'id': id}).fetchone()[0]

            # Ensure valid input for stock levels
            try:
                stock = int(request.form.get('stock'))
                # Zero does not change anything
                if stock == 0:
                    flash('Invalid stock input')
                    return redirect('/books')
                # Stock level can not be set to 0 or below
                if (current_stock + stock) < 1:
                    flash('Stock level of a book can not be set to 0, use remove option instead')
                    return redirect('/books')
                # Current availability of a book can not be reduced below 0
                if (available + stock) < 0:
                    flash(f'Not enough currently available copies ({available}) of a book in library, please wait until they are returned')
                    return redirect('/books')
            except:
                flash('Invalid stock input')
                return redirect('/books')

            # Ensure all details are provided
            if not title or not author or not genre or not year:
                flash('All fields are required')
                return redirect('/books')

            # Update books table
            db.session.execute(text('UPDATE books SET title = :title, author = :author, genre = :genre, year = :year, stock = :stock, available = :available WHERE id = :id'),
                               {'title': title, 'author': author, 'genre': genre, 'year': year, 'stock': current_stock + stock, 'available': available + stock, 'id': id})
            db.session.commit()

            # Flash a message
            flash(f'Book ID:{id} details updated!')

            # Redirect to books route and show updated table
            return redirect('/books')

        
    
@app.route('/new-book', methods=['GET', 'POST'])
@login_required
def new_book():
    '''Add new book'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name_result = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()
    if name_result:
        name = name_result[0]
    else:
        flash('User not found')
        return redirect('/login')

    if request.method == 'POST':
        # User input
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        year = request.form.get('year')

        # Ensure all details are provided
        if not title or not author or not genre or not year:
            flash('All fields are required')
            return redirect('/new-book')

        # Ensure valid input for stock
        try:
            stock = int(request.form.get('stock'))
            if stock < 1:
                flash('Invalid stock input')
                return redirect('/new-book')
        except ValueError:
            flash('Invalid stock input')
            return redirect('/new-book')

        try:
            # Check if the book already exists
            existing_book = db.session.execute(text('SELECT id FROM books WHERE title = :title AND author = :author'),
                                               {'title': title, 'author': author}).fetchone()
            if existing_book:
                flash('This book already exists.')
                return redirect('/new-book')

            # Insert new book details into books table without specifying the id
            db.session.execute(text('INSERT INTO books (title, author, genre, year, stock, available) VALUES (:title, :author, :genre, :year, :stock, :available)'),
                               {'title': title, 'author': author, 'genre': genre, 'year': year, 'stock': stock, 'available': stock})
            db.session.commit()

            # Flash book added message on redirect
            flash(f'A book "{title}" by "{author}" has been added.')

            # Redirect to manage books route
            return redirect('/catalogue')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {str(e)}')
            return redirect('/new-book')

    # User reached route via GET, render new_book template
    return render_template('new-book.html', name=name, genres=GENRES)



@app.route('/members', methods=['GET', 'POST'])
@login_required
def members():
    '''Members management'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()[0]

    # Query database for members ordered by name
    members = db.session.execute(text('SELECT * FROM members WHERE deleted = :deleted ORDER BY name ASC'), {'deleted': 0}).fetchall()

    # Convert the result to a list of dictionaries
    members = [dict(row._asdict()) for row in members]
    
    # User reached route via GET
    if request.method == 'GET':

        # Search members query and selected field
        query = request.args.get('query')
        field = request.args.get('field')

        # Query exists and search by field is 'id', return exact match as JSON response
        if query and field == 'member_id':
            match = db.session.execute(text('SELECT * FROM members WHERE deleted = :deleted AND member_id = :member_id'), {'deleted': 0, 'member_id': query}).fetchall()
            return jsonify(match)
        
        # Any other search field selected
        elif query and field != 'member_id':
            # Populate matches list and return JSON response with matching items
            matches = [member for member in members if query.lower() in str(member[field]).lower()]
            return jsonify(matches)
        
        # Render members.html
        return render_template('members.html', name=name, members=members)

    # User reached route via POST
    else:
        # Get the value of the button user clicked on
        button = request.form.get('button')
        
        # Remove button selected
        if button == 'remove':
            
            # Query database for a name of a member to be deleted
            removed = db.session.execute(text('SELECT name FROM members WHERE member_id = :member_id'), {'member_id': request.form.get('id')}).fetchone()[0]

            # Delete member (tag as deleted)
            db.session.execute(text('UPDATE members SET deleted = :deleted WHERE member_id = :member_id'), {'deleted': 1, 'member_id': request.form.get('id')})

            # Flash a message
            flash(f'Member {removed} has been removed.')

            # Redirect to members route with updated table
            return redirect('/members')
        
        # Update button selected on a popup form
        elif button == 'update':

            # User input
            id = request.form.get("form_id")
            member = request.form.get('name')
            email = request.form.get('email')
            address = request.form.get('address')
            phone = request.form.get('phone')

            # Ensure all details provided
            if not member or not email or not address or not phone:
                flash('All fields are required')
                return render_template('members.html', name=name, members=members)

            # Update members table
            db.session.execute(text('UPDATE members SET name = :name, email = :email, address = :address, phone = :phone WHERE member_id = :member_id'), {'name': member, 'email': email, 'address': address, 'phone': phone, 'member_id': id})
            
            flash(f'Member ID:{id} details updated!')
            
            # Redirect to members route and show updated table
            return redirect('/members')
        
     
@app.route('/new-member', methods=['GET', 'POST'])
@login_required
def new_member():
    '''Add new member'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()[0]

    # User reached route via GET
    if request.method == 'GET':
        return render_template('new-member.html', name=name)
    
    # User reached route via POST
    else:
        # User input
        member = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Ensure all details are provided
        if not member or not email or not address or not phone:
            flash('All fields are required')
            return render_template('new-member.html', name=name)        

        # Insert new member details into members table
        insert_query = text('INSERT INTO members (name, email, address, phone, borrowed) VALUES (:member, :email, :address, :phone, 0)')
        db.session.execute(insert_query, {'member': member, 'email': email, 'address': address, 'phone': phone})
        db.session.commit()
        
        # Flash member added message on redirect
        flash(f'A member {member} joins the library.')
       
        # Redirect to members route
        return redirect('/members')
    

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    '''Lending books to members'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()[0]

    # Pre-fetch members and books to be used in both GET and POST requests
    members = db.session.execute(text('SELECT * FROM members WHERE deleted = :deleted'), {'deleted': 0}).fetchall()
    books = db.session.execute(text('SELECT * FROM books WHERE deleted = :deleted'), {'deleted': 0}).fetchall()
    transactions = db.session.execute(text('SELECT * FROM transactions')).fetchall()

    # User reached route via GET
    if request.method == 'GET':
        queryMember = request.args.get('queryMember')
        queryBook = request.args.get('queryBook')

        # User searched for members
        if queryMember:
            members_list = [
                {
                    'member_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'address': row[3],
                    'phone': row[4],
                    'borrowed': row[5],
                    'created_at': row[6],
                    'deleted': row[7]
                } for row in members
            ]
            return jsonify(members_list)

        # User searched for books
        if queryBook:
            books_list = [
                {
                    'id': row[0],
                    'title': row[1],
                    'author': row[3],
                    'genre': row[4],
                    'year': row[5],
                    'available': row[6]
                } for row in books
            ]

            transactions_list = [
                {
                    'borrower_id': row[0],
                    'book_id': row[1],
                    'type': row[2],
                    'employee_id': row[3],
                    'created_at': row[4]
                } for row in transactions if len(row) >= 5
            ]
            return jsonify({'books': books_list, 'transactions': transactions_list})

        return render_template('checkout.html', name=name)

    # User reached route via POST
    else:
        memberId = request.form.get('memberId')
        bookIds = request.form.getlist('bookId')

        for id in bookIds:
            available = db.session.execute(text('SELECT available FROM books WHERE id = :id'), {'id': id}).fetchone()[0]
            borrowed = db.session.execute(text('SELECT borrowed FROM members WHERE member_id = :memberId'), {'memberId': memberId}).fetchone()[0]

            # Only process if the book is available
            if available > 0:
                db.session.execute(text('INSERT INTO transactions (borrower_id, book_id, type, employee_id) VALUES (:memberId, :id, :type, :user_id)'),
                                   {'memberId': memberId, 'id': id, 'type': 'borrow', 'user_id': user_id})

                db.session.execute(text('UPDATE books SET available = :available WHERE id = :id'), {'available': available - 1, 'id': id})
                db.session.execute(text('UPDATE members SET borrowed = :borrowed WHERE member_id = :memberId'), {'borrowed': borrowed + 1, 'memberId': memberId})

        db.session.commit()

        member_name = db.session.execute(text('SELECT name FROM members WHERE member_id = :memberId'), {'memberId': memberId}).fetchone()[0]
        flash(f'Books successfully checked out to {member_name}')
        return redirect('/')


@app.route('/history')
@login_required
def history():
    '''Transactions history'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    name = db.session.execute(text('SELECT name FROM staff WHERE staff_id = :user_id'), {'user_id': user_id}).fetchone()[0]

    # Query database for all transactions and join other tables
    transactions = db.session.execute(text('''
        SELECT transactions.*, members.name AS member_name, books.title, staff.name AS staff_name
        FROM transactions
        JOIN books ON books.id = transactions.book_id
        JOIN members ON members.member_id = transactions.borrower_id
        JOIN staff ON staff.staff_id = transactions.employee_id
        ORDER BY transactions.time DESC
    ''')).fetchall()

    return render_template('history.html', name=name, transactions=transactions)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Register new librarian'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    staff = Staff.query.filter_by(staff_id=user_id).first()

    # User reached route via POST
    if request.method == 'POST':

        # User input
        name = request.form.get('name')
        user_name = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Ensure all fields provided
        if not name or not user_name or not password:
            flash('All fields required')
            return redirect('/register')

        # Username already in database (even if tagged as deleted)
        elif Staff.query.filter_by(username=user_name).first():
            flash('Username already exists')
            return redirect('/register')

        # Ensure password is at least 4 characters long
        if len(password) < 4:
            flash('Password must be at least four characters long')
            return redirect('/register')
        
        # Ensure password and confirmation password match
        elif password != confirmation:
            flash('Password and confirmation password do not match')
            return redirect('/register')
        
        # Generate hash for password
        hash = generate_password_hash(password)

        # Store name, username and password hash into database
        new_staff = Staff(name=name, username=user_name, hash=hash)
        db.session.add(new_staff)
        db.session.commit()
        
        # Redirect user
        flash('New librarian has been added')
        return redirect('/register')
    
    # Route reached via GET
    return render_template('/register.html', name=staff.name if staff else '')



@app.route('/remove', methods=['GET', 'POST'])
def remove():
    '''Remove librarian'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    staff = Staff.query.filter_by(staff_id=user_id).first()
    name = staff.name if staff else "Unknown"

    # Query database for all librarians except admin
    staff_list = Staff.query.filter(Staff.staff_id != 1, Staff.deleted == 0).all()

    # Route reached via POST
    if request.method == 'POST':

        # User selection
        staff_id = request.form.get('remove')

        # Query database for librarian name
        librarian = Staff.query.filter_by(staff_id=staff_id).first()
        l_name = librarian.name if librarian else "Unknown"

        # Remove librarian (tag as deleted)
        librarian.deleted = 1
        db.session.commit()

        # Flash a message on removal
        flash(f'Librarian {l_name} has been removed from LMS')

        return redirect('/remove')

    # Route reached via GET
    return render_template('remove.html', name=name, staff=staff_list)

        
    
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    '''Password change'''

    # Get the user ID from the session
    user_id = session.get('user_id')

    # Query the database for the current user
    staff = Staff.query.filter_by(staff_id=user_id).first()

    # If the user is not found, handle it accordingly
    if not staff:
        flash('User not found')
        return redirect('/login')

    # Get the user's name
    name = staff.name

    # Route reached via POST
    if request.method == 'POST':
        # User input
        old_pass = request.form.get('old_pass')
        new_pass = request.form.get('new_pass')
        confirm_pass = request.form.get('confirm_pass')

        # Check if the old password matches the current password
        if not check_password_hash(staff.hash, old_pass):
            flash('Invalid password')
            return redirect('/account')

        # Ensure all fields provided
        if not old_pass or not new_pass:
            flash('All fields required')
            return redirect('/account')

        # Ensure password is at least 4 characters long
        if len(new_pass) < 4:
            flash('Password must be at least four characters long')
            return redirect('/account')

        # Ensure new password matches confirm password
        elif new_pass != confirm_pass:
            flash('New password and confirmation password do not match')
            return redirect('/account')

        # Generate hash for the new password
        hash = generate_password_hash(new_pass)

        # Update the user's password
        staff.hash = hash
        db.session.commit()

        flash('Password changed')

        return redirect('/account')

    # Route reached via GET
    return render_template('account.html', name=name)
    


@app.route('/faq')
@login_required
def faq():
    '''Frequently asked questions'''

    # Get user_id from session
    user_id = session['user_id']

    # Query database for librarian name
    staff = Staff.query.filter_by(staff_id=user_id).first()

    if staff:
        name = staff.name
    else:
        name = "Unknown"

    return render_template('faq.html', name=name)




# Main driver function
if __name__ == '__main__':
    app.run()