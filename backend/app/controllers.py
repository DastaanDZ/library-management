# controllers.py
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, Blueprint, jsonify
import pdfkit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, Book, Request, Feedback, Section, IssuedBook
from app.database import db
from datetime import datetime, timedelta
from tasks import send_email

app = Blueprint('controllers', __name__)

@app.route('/', methods=['GET'])
def greeting():
    return("Hello, world")

@app.route('/email', methods=['GET'])
def mail():
    send_email.delay("21f2001529@ds.study.iitm.ac.in","nigaver985@ikumaru.com","Test subject","This is a test message")
    return("EMAIL sent")

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    new_user.save()
    return jsonify({'message': 'User created successfully!'}), 201

# Endpoint to get user info
@jwt_required()
@app.route('/user-info/<int:user_id>', methods=['GET'])
def user_info(user_id):

    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_info = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }

    return jsonify(user_info), 200

@jwt_required()
@app.route('/edit-user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Update user attributes
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            # Hash the new password before updating
            hashed_password = generate_password_hash(data['password'], method='sha256')
            user.password = hashed_password
        if 'role' in data:
            user.role = data['role']
        # Add more attributes as needed

        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401

    user.last_login = datetime.now()  # Update last login time
    db.session.commit()  # Commit changes to the database

    access_token = create_access_token(identity=user.id)
    print(access_token)
    return jsonify({'access_token': access_token, 'role': user.role}), 200


@app.route('/sections', methods=['GET'])
@jwt_required()
def view_sections():
    sections = Section.query.all()
    return jsonify({'sections': [section.serialize() for section in sections]}), 200

# Request a book
@app.route('/request-book/<int:book_id>', methods=['POST'])
@jwt_required()
def request_book(book_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    book = Book.query.get(book_id)
    
    # Check if the book is already requested by the user
    if Request.query.filter_by(user_id=user_id, book_id=book_id).first():
        return jsonify({'message': 'You have already requested this book'}), 400
            
    # Create a request for the book
    request = Request(user_id=user_id, book_id=book_id)
    db.session.add(request)
    db.session.commit()
    
    return jsonify({'message': 'Book requested successfully'}), 201

@app.route('/requested-books/<int:user_id>', methods=['GET'])
@jwt_required()
def get_requested_books(user_id):

    # Query the database to retrieve the list of requested books for the user
    requested_books = Request.query.filter_by(user_id=user_id).all()

    # Initialize an empty list to store serialized requested book data
    requested_books_data = []

    # Loop through each requested book and serialize its data
    for request in requested_books:
        # Query the Book model to get the details of the requested book
        book = Book.query.get(request.book_id)
        if book:
            # Serialize the requested book data along with additional book details
            requested_book_data = {
                'id': request.id,
                'user_id': request.user_id,
                'book_id': request.book_id,
                'name': book.name,
                'author': book.author,
                # Add more book details as needed
            }
            # Append the serialized requested book data to the list
            requested_books_data.append(requested_book_data)
    print(requested_books_data)
    # Return the serialized requested books data as a JSON response
    return jsonify(requested_books_data), 200

@app.route('/issued-books/<int:user_id>', methods=['GET'])
def get_issued_books(user_id):
    issued_books = IssuedBook.query.filter_by(user_id=user_id).all()

    # Initialize an empty list to store serialized issued book data
    issued_books_data = []

    # Loop through each issued book and serialize its data
    for issued_book in issued_books:
        # Query the Book model to get the details of the issued book
        book = Book.query.get(issued_book.book_id)
        if book:
            # Serialize the issued book data along with additional book details
            issued_book_data = {
                'id': issued_book.id,
                'user_id': issued_book.user_id,
                'book_id': issued_book.book_id,
                'name': book.name,
                'author': book.author,
                'issue_date': issued_book.issue_date.strftime('%Y-%m-%d %H:%M:%S'),
                'return_date': issued_book.return_date.strftime('%Y-%m-%d %H:%M:%S') if issued_book.return_date else None,
                # Add more book details as needed
            }
            # Append the serialized issued book data to the list
            issued_books_data.append(issued_book_data)

    # Return the serialized issued books data as a JSON response
    return jsonify(issued_books_data), 200

# Return a book
@app.route('/return-book/<int:book_id>', methods=['POST'])
@jwt_required()
def return_book(book_id):
    user_id = get_jwt_identity()
    request = Request.query.filter_by(user_id=user_id, book_id=book_id).first()
    
    if not request:
        return jsonify({'message': 'You have not requested this book'}), 400
    
    db.session.delete(request)
    db.session.commit()
    
    return jsonify({'message': 'Book returned successfully'}), 200

# Give feedback for a book
@app.route('/feedback/<int:book_id>', methods=['POST'])
@jwt_required()
def give_feedback(book_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    feedback_text = data.get('feedback_text')
    
    feedback = Feedback(user_id=user_id, book_id=book_id, feedback_text=feedback_text)
    db.session.add(feedback)
    db.session.commit()
    
    return jsonify({'message': 'Feedback submitted successfully'}), 201

@app.route('/add-book', methods=['POST'])
@jwt_required()
def add_book():
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can add books'}), 403

    data = request.get_json()
    name = data.get('name')
    content = data.get('content')
    author = data.get('author')
    count = data.get('count')
    available = data.get('available')
    price = data.get('price')

    if not all([name, content, author, count, available, price]):
        return jsonify({'message': 'Missing required data'}), 400

    new_book = Book(name=name, content=content, author=author, count=count, available= available, price=price)
    # Add more attributes as needed

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully', 'book_id': new_book.id}), 201

@app.route('/issue-book/<int:user_id>', methods=['POST'])
@jwt_required()
def issue_book(user_id):
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can issue books'}), 403
    
    data = request.get_json()
    book_ids = data.get('book_ids', [])

    for book_id in book_ids:
        book = Book.query.get(book_id)
        if book and book.available:
            issued_book = IssuedBook(user_id=user_id, book_id=book_id, librarian_id=1)
            book.count -= 1
            if book.count == 0:
                book.available = False
            db.session.add(issued_book)
            db.session.commit()
        else:
            return jsonify({'message': 'Book not found or already issued'}), 404
    
    return jsonify({'message': 'Books issued successfully'}), 200

# Revoke access for e-book(s) from a user
@app.route('/revoke-access/<int:user_id>', methods=['POST'])
@jwt_required()
def revoke_access(user_id):
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can revoke access'}), 403
    
    data = request.get_json()
    book_ids = data.get('book_ids', [])

    for book_id in book_ids:
        issued_book = IssuedBook.query.filter_by(user_id=user_id, book_id=book_id).first()
        if issued_book:
            book = Book.query.get(book_id)
            book.count += 1
            if not book.available:
                book.available = True
            db.session.delete(issued_book)
            db.session.commit()
        else:
            return jsonify({'message': 'Book not found or not issued to the user'}), 404
    
    return jsonify({'message': 'Access revoked successfully'}), 200

# Edit an existing section/e-book
@app.route('/edit-book/<int:book_id>', methods=['PUT'])
@jwt_required()
def edit_book(book_id):
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can edit books'}), 403
    
    data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Update book attributes
    if 'name' in data:
        book.name = data['name']
    if 'content' in data:
        book.content = data['content']
    if 'author' in data:
        book.author = data['author']
    if 'count' in data:
        book.count = data['count']
    if 'available' in data:
        book.available = data['available']
    if 'price' in data:
        book.price = data['price']
    # Add more attributes as needed

    db.session.commit()
    return jsonify({'message': 'Book updated successfully'}), 200

# Remove an existing section/e-book
@app.route('/remove-book/<int:book_id>', methods=['DELETE'])
@jwt_required()
def remove_book(book_id):
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can remove books'}), 403
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book removed successfully'}), 200

# Assign a book to a particular section
@app.route('/assign-book/<int:book_id>/<int:section_id>', methods=['POST'])
@jwt_required()
def assign_book(book_id, section_id):
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can assign books'}), 403
    
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    section = Section.query.get(section_id)
    if not section:
        return jsonify({'message': 'Section not found'}), 404

    book.section_id = section_id
    db.session.commit()
    return jsonify({'message': 'Book assigned to section successfully'}), 200

# Monitor current status of each e-book and the user it is issued to
@app.route('/monitor', methods=['GET'])
@jwt_required()
def monitor():
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can monitor'}), 403
    
    issued_books = IssuedBook.query.all()
    monitored_books = []
    for issued_book in issued_books:
        book = Book.query.get(issued_book.book_id)
        user = User.query.get(issued_book.user_id)
        monitored_books.append({
            'book_name': book.name,
            'user_name': user.username,
            'issue_date': issued_book.issue_date.strftime('%Y-%m-%d'),
            'return_date': issued_book.return_date.strftime('%Y-%m-%d') if issued_book.return_date else None
        })

    return jsonify({'monitored_books': monitored_books}), 200

# View available e-books in the Library
@app.route('/available-books', methods=['GET'])
@jwt_required()
def view_available_books():
    librarian_id = get_jwt_identity()
    librarian = User.query.get(librarian_id)
    if librarian.role != 'librarian':
        return jsonify({'message': 'Only librarians can view available books'}), 403
    
    available_books = Book.query.filter_by(available=True).all()
    return jsonify({'available_books': [book.serialize() for book in available_books]}), 200


@app.route('/books')
@jwt_required()
def list_books():
    books = Book.query.all()
    # Serialize each book object
    # print(books)
    serialized_books = [book.serialize() for book in books]
    print(serialized_books)
    return jsonify(serialized_books)


@app.route('/buy/<int:book_id>')
@jwt_required()
def buy(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)

    generate_pdf(book)
    return redirect(url_for('download', book_id=book_id))

@app.route('/download/<int:book_id>')
@jwt_required()
def download(book_id):
    book = Book.query.get(book_id)
    if not book:
        abort(404)

    return send_from_directory('pdfs', f'{book.name}.pdf')

def generate_pdf(book):
    html_content = f"""
    <html>
    <head><title>{book.name}</title></head>
    <body>
        <h1>{book.name}</h1>
        <p>Price: ${book.price}</p>
        <p>Description: Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        <!-- Add more book details here -->
    </body>
    </html>
    """
    pdfkit.from_string(html_content, f'pdfs/{book.name}.pdf')


@app.route('/books/<int:book_id>', methods=['GET'])
@jwt_required()
def get_book_details(book_id):
    # Query the database to retrieve the book details based on the provided ID
    book = Book.query.get(book_id)

    if not book:
        # If book with the provided ID is not found, return a 404 Not Found response
        return jsonify({'message': 'Book not found'}), 404

    # Serialize the book object into JSON format
    book_details = book.serialize()

    # Return the book details in JSON format
    return jsonify(book_details), 200


@app.route('/sections', methods=['GET'])
def search_section():
    query = request.args.get('query')  # Get the search query from the request parameters
    sections = Section.query.filter(Section.name.ilike(f'%{query}%')).all()  # Search for sections containing the query
    serialized_sections = [section.serialize() for section in sections]  # Serialize sections
    return jsonify(serialized_sections), 200

@app.route('/books', methods=['GET'])
def search_books():
    query = request.args.get('query')  # Get the search query from the request parameters
    books = Book.query.filter(
        (Book.name.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%')) |
        (Book.content.ilike(f'%{query}%'))
    ).all()  # Search for books containing the query in name, author, or content
    serialized_books = [book.serialize() for book in books]  # Serialize books
    return jsonify(serialized_books), 200