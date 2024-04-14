
from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, Blueprint, jsonify
import pdfkit
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from app.models import User, Book, Request, Feedback, Section, IssuedBook
from app.database import db
from datetime import datetime, timedelta

app = Blueprint('controllers', __name__)

@app.route('/', methods=['GET'])
def greeting():
    return("Hello, world")

@app.route('/inactive-users', methods=['GET'])
def get_inactive_users_endpoint():

    inactive_threshold = datetime.now() - timedelta(seconds=5)

    inactive_users = User.query.filter(User.last_login < inactive_threshold).all()

    serialized_users = [{'id': user.id, 'username': user.username, 'email': user.email} for user in inactive_users]
    
    return jsonify({'inactive_users': serialized_users}), 200

@app.route('/check-inactive', methods=['GET'])
def checkInactive():

    inactive_threshold = datetime.now() - timedelta(seconds=5)

    inactive_users = User.query.filter(User.last_login < inactive_threshold).all()

    print("INACTIVE USERS:")
    for user in inactive_users:
        print("SENDING REMINDER TO:", user.username)

    return("SENDING DONE")
    

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = User.query.filter_by(username=data['username']).first()
    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_user or existing_email:
        return jsonify({'error': 'Username already exists!'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, role=data['role'])
    new_user.save()
    return jsonify({'message': 'User created successfully!'}), 201

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

        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            hashed_password = generate_password_hash(data['password'])
            user.password = hashed_password
        if 'role' in data:
            user.role = data['role']

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

    user.last_login = datetime.now() 
    db.session.commit()  

    access_token = create_access_token(identity=user.id)
    print(access_token)
    return jsonify({'access_token': access_token, 'role': user.role}), 200

@app.route('/logout', methods=['POST'])
@jwt_required()  
def logout():

    current_user_id = get_jwt_identity()

    resp = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(resp)
    
    return resp, 200

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
    
    if Request.query.filter_by(user_id=user_id, book_id=book_id).first():
        return jsonify({'message': 'You have already requested this book'}), 400

    request = Request(user_id=user_id, book_id=book_id)
    db.session.add(request)
    db.session.commit()
    
    return jsonify({'message': 'Book requested successfully'}), 201

@app.route('/requested-books/<int:user_id>', methods=['GET'])
@jwt_required()
def get_requested_books(user_id):

    requested_books = Request.query.filter_by(user_id=user_id).all()

    requested_books_data = []

    for request in requested_books:

        book = Book.query.get(request.book_id)
        if book:
            requested_book_data = {
                'id': request.id,
                'user_id': request.user_id,
                'book_id': request.book_id,
                'name': book.name,
                'author': book.author,
                'link': book.link,

            }

            requested_books_data.append(requested_book_data)
    print(requested_books_data)

    return jsonify(requested_books_data), 200

@app.route('/issued-books/<int:user_id>', methods=['GET'])
def get_issued_books(user_id):
    issued_books = IssuedBook.query.filter_by(user_id=user_id).all()


    issued_books_data = []

    for issued_book in issued_books:

        book = Book.query.get(issued_book.book_id)
        if book:

            issued_book_data = {
                'id': issued_book.id,
                'user_id': issued_book.user_id,
                'book_id': issued_book.book_id,
                'name': book.name,
                'author': book.author,
                'issue_date': issued_book.issue_date.strftime('%Y-%m-%d %H:%M:%S'),
                'return_date': issued_book.return_date.strftime('%Y-%m-%d %H:%M:%S') if issued_book.return_date else None,
                'link': book.link,

            }
        
            issued_books_data.append(issued_book_data)

    return jsonify(issued_books_data), 200

# Return a book
@app.route('/return-book/<int:book_id>', methods=['POST'])
@jwt_required()
def return_book(book_id):
    user_id = get_jwt_identity()

    if user_id is None or book_id is None:
        return jsonify({'message': 'User ID and Book ID are required'}), 400

    issued_book = IssuedBook.query.filter_by(user_id=user_id, book_id=book_id).first()
    
    if not issued_book:
        return jsonify({'message': 'You have not issued this book'}), 400

    db.session.delete(issued_book)
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
    link = data.get('selectedFile')
    if not all([name, content, author, count, available, price,link]):
        return jsonify({'message': 'Missing required data'}), 400

    new_book = Book(name=name, content=content, author=author, count=count, available= available, price=price, link=link)

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
    
    print("ISSUING BOOK")
    
    data = request.get_json()
    book_ids = data.get('book_id', [])

    print("GOT BOOK", book_ids)

    for book_id in book_ids:
        book = Book.query.get(book_id)
        if book and book.available:
            issued_book = IssuedBook(user_id=user_id, book_id=book_id, librarian_id=librarian_id)
            print("ISSUED BOOKS", issued_book)
            book.count -= 1
            if book.count == 0:
                book.available = False
            db.session.add(issued_book)
            db.session.commit()
            print("COMMITED")
        else:
            return jsonify({'message': 'Book not found or already issued'}), 404
    
    return jsonify({'message': 'Books issued successfully'}), 200

# Revoke access for e-book(s) from a user
@app.route('/revoke-access', methods=['POST'])
def revoke_access():

    data = request.get_json()
    book_id = data.get('book_id')
    user_id = data.get('user_id')

    if not book_id or not user_id:
        return jsonify({'message': 'Both book_id and user_id are required.'}), 400

    issued_book = IssuedBook.query.filter_by(book_id=book_id, user_id=user_id).first()

    if issued_book:
        db.session.delete(issued_book)
        db.session.commit()
        return jsonify({'message': 'Access revoked successfully.'}), 200
    else:
        return jsonify({'message': 'No access found for the provided book and user.'}), 404

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

@app.route('/monitor', methods=['GET'])
@jwt_required()
def monitor_books():

    books = Book.query.all()

    monitored_books = []

    for book in books:

        issued_books = IssuedBook.query.filter_by(book_id=book.id).all()

        available = len(issued_books) == 0 

        users_issued_to = []

        for issued_book in issued_books:
            user = User.query.get(issued_book.user_id)
            user_feedback = Feedback.query.filter_by(user_id=user.id,book_id=book.id).first()
            users_issued_to.append({
                'id': user.id,
                'name': user.username,
                'feedback': user_feedback.feedback_text if user_feedback else None
            })

        book_info = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'available': available,
            'users_issued_to': users_issued_to

        }

        monitored_books.append(book_info)

    return jsonify(monitored_books)




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

    book = Book.query.get(book_id)
    print(book)
    if not book:

        return jsonify({'message': 'Book not found'}), 404

    book_details = book.serialize()
    return jsonify(book_details), 200


@app.route('/sections', methods=['GET'])
def search_section():
    query = request.args.get('query')  
    sections = Section.query.filter(Section.name.ilike(f'%{query}%')).all()  
    serialized_sections = [section.serialize() for section in sections]  
    return jsonify(serialized_sections), 200

@app.route('/books', methods=['GET'])
def search_books():
    query = request.args.get('query') 
    books = Book.query.filter(
        (Book.name.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%')) |
        (Book.content.ilike(f'%{query}%'))
    ).all() 
    serialized_books = [book.serialize() for book in books] 
    return jsonify(serialized_books), 200


@app.route('/users-requested/<int:book_id>', methods=['GET'])
@jwt_required()
def get_users_requested(book_id):
    requests = Request.query.filter_by(book_id=book_id).all()
    requested_users = [request.user_id for request in requests]

    return jsonify({'requested_users' : requested_users}), 200

@app.route('/unique-books-requested', methods=['GET'])
def unique_books_requested():
 
    distinct_book_ids = db.session.query(Request.book_id).distinct().all()

    unique_books = []
    for book_id in distinct_book_ids:
        book = Book.query.get(book_id)
        if book:
            unique_books.append({
                'id': book.id,
                'name': book.name,
                'author': book.author,
                'link': book.link,
                'content': book.content,
                'price': book.price,
    
            })

    return jsonify({'unique_books': unique_books}), 200


@app.route('/remove-request/<int:request_id>', methods=['DELETE'])
def remove_request(request_id):
    request_entry = Request.query.get(request_id)
    if not request_entry:
        return jsonify({'message': 'Request not found'}), 404


    db.session.delete(request_entry)
    db.session.commit()

    return jsonify({'message': 'Request removed successfully'}), 200

@app.route('/request-id', methods=['GET'])
def get_request_id():

    book_id = request.args.get('book_id')
    user_id = request.args.get('user_id')

    if not book_id or not user_id:
        return jsonify({'message': 'Missing book_id or user_id parameter'}), 400

    request_entry = Request.query.filter_by(book_id=book_id, user_id=user_id).first()

    if not request_entry:
        return jsonify({'message': 'Request not found'}), 404

    return jsonify({'request_id': request_entry.id}), 200

@app.route('/add-section', methods=['POST'])
@jwt_required()
def add_section():

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'message': 'Name is required for the section'}), 400

    new_section = Section(name=name, description=description, date_created=datetime.utcnow())
    db.session.add(new_section)
    db.session.commit()
    return jsonify({'message': 'Section added successfully', 'section_id': new_section.id}), 201
    
# Endpoint to fetch the number of books issued to a user
@app.route('/books-issued/<int:user_id>', methods=['GET'])
def books_issued(user_id):
    issued_books_count = IssuedBook.query.filter_by(user_id=user_id).count()
    return jsonify({'count': issued_books_count}), 200

# Endpoint to fetch the number of book requests made by a user
@app.route('/books-requested/<int:user_id>', methods=['GET'])
def books_requested(user_id):
    requested_books_count = Request.query.filter_by(user_id=user_id).count()
    return jsonify({'count': requested_books_count}), 200

# Endpoint to fetch issued books and feedbacks filtered by start and end dates
@app.route('/reports/<int:user_id>', methods=['GET'])
def fetch_reports(user_id):
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    if not start_date_str or not end_date_str:
        return jsonify({'message': 'Both start_date and end_date are required as query parameters.'}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD format.'}), 400

    issued_books = IssuedBook.query.filter(IssuedBook.issue_date >= start_date, IssuedBook.issue_date < end_date, IssuedBook.user_id == user_id).all()
    feedbacks = Feedback.query.filter(Feedback.created_at >= start_date, Feedback.created_at < end_date,Feedback.user_id == user_id).all()

    serialized_issued_books = [book.serialize() for book in issued_books]
    serialized_feedbacks = [feedback.serialize() for feedback in feedbacks]

    return jsonify({'issued_books': serialized_issued_books, 'feedbacks': serialized_feedbacks}), 200

# Endpoint to fetch all users
@app.route('/all-users', methods=['GET'])
def get_all_users():
    users = User.query.all()  
    user_list = []
    for user in users:
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
        user_list.append(user_info)
    return jsonify(users=user_list), 200