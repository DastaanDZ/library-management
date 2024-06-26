from app.database import db
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False) 
    last_login = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()


class Book(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer())
    available = db.Column(db.Boolean())
    price = db.Column(db.Integer(), nullable=False)
    link = db.Column(db.String(), nullable=False)
  
    section_id = db.Column(db.Integer(), db.ForeignKey('section.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'author': self.author,
            'count': self.count,
            'available': self.available,
            'price': self.price,
            'link': self.link,
  
        }


class Feedback(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'))
    feedback_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

class Section(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.Text)
    
    books = db.relationship('Book', backref='section', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created.strftime('%Y-%m-%d'),
            'description': self.description,
            'books': [book.serialize() for book in self.books] 
        }
    

class IssuedBook(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'))
    librarian_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'librarian_id': self.librarian_id,
            'issue_date': self.issue_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': self.return_date.strftime('%Y-%m-%d %H:%M:%S') if self.return_date else None
        }


class Request(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer(), db.ForeignKey('book.id'))

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id
        }