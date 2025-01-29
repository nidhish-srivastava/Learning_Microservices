from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///authors.db'
db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(200),nullable = False)
    birthdate = db.Column(db.String(200))

@app.route('/authors',methods=['POST'])
def add_author():
    data = request.get_json()
    new_author = Author(
        name = data['name'],
        email = data['email'],
        birthdate = data.get('birthdate','')
    )
    db.session.add(new_author)    
    db.session.commit()
    return jsonify({'message' : 'Author created successfully'}),201

@app.route('/authors/<int:id>',methods=['GET'])
def get_author(id):
    author = Author.get_or_404(id)
    return jsonify({'id' : author.id,'name' : author.name,'email' : author.email,'birthdate' : author.birthdate})

@app.route('/authors',methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return jsonify([{
        'id' : author.id,'name' : author.name,'email' : author.email,'birthdate' : author.birthdate
    } for author in authors])

@app.route('/authors',methods=['PUT'])
def update_author(id):
    author = Author.query.get_or_404(id)
    data = request.get_json()
    data.name = data.get('name',author.name)
    data.email = data.get('email',author.email)
    data.birthdate = data('birthdate',author.birthdate)
    db.session.commit()
    return jsonify({'message' : 'Author updated successfully!'})

@app.route('/authors/<int:id>',methods=['DELETE'])
def delete_author(id):
    author = Author.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    return jsonify({'message' : 'Author deleted successfully'})

if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()  # Ensure tables are created
    app.run(debug=True, port=5001)
