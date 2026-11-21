from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'{self.book_name} - {self.author} - {self.publisher}'


@app.route('/book', methods=['GET'])
def get_book():
    books = Book.query.all()
    
    output = []
    for book in books:
        book_data = {
            'book_id': book.id, 
            'book_name': book.book_name, 
            'author': book.author, 
            'publisher': book.publisher
        }
        
        output.append(book_data)
        
    return {"books": output}

@app.route('/book/<id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.query.get_or_404(id)
    
    return {
        'book_id': book.id, 
        'book_name': book.book_name, 
        'author': book.author, 
        'publisher': book.publisher
    }

@app.route('/book', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {
        'book_id': book.id,
        'book_name': book.book_name,
        'author': book.author,
        'publisher': book.publisher
    }
    
@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    if book is None:
        return {"message": "Book not found"}, 404
    db.session.delete(book)
    db.session.commit()
    
    return {"message": "Book deleted successfully"}