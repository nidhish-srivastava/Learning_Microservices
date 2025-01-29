from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    published_date = db.Column(db.String(100))
    isbn = db.Column(db.String(50), unique=True, nullable=False)
    publisher_name = db.Column(db.String(200))

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(
        title=data['title'], author_id=data['author_id'],
        published_date=data.get('published_date', ''), isbn=data['isbn'],
        publisher_name=data.get('publisher_name', '')
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author_id': book.author_id,
                     'published_date': book.published_date, 'isbn': book.isbn,
                     'publisher_name': book.publisher_name} for book in books])

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({'id': book.id, 'title': book.title, 'author_id': book.author_id,
                    'published_date': book.published_date, 'isbn': book.isbn,
                    'publisher_name': book.publisher_name})

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author_id = data.get('author_id', book.author_id)
    book.published_date = data.get('published_date', book.published_date)
    book.isbn = data.get('isbn', book.isbn)
    book.publisher_name = data.get('publisher_name', book.publisher_name)
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'})

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()  # Ensure tables are created
    app.run(debug=True, port=5001)
