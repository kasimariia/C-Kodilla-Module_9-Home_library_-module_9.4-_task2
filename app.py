from flask import Flask, jsonify, request, abort, render_template
import os
import json

app = Flask(__name__)

# Завантаження даних про книги з файлу JSON
def load_books():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "books.json"))
    try:
        with open(file_path, "r") as f:
            return json.load(f)["library"]
    except FileNotFoundError:
        return []

# Збереження даних про книги до файлу JSON
def save_books(books):
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "books.json"))
    with open(file_path, 'w') as file:
        json.dump({"library": books}, file)

# Отримати список всіх книг
@app.route('/api/books', methods=['GET'])
def get_books():
    books = load_books()
    return jsonify(books)

# Додати нову книгу
@app.route('/api/books', methods=['POST'])
def create_book():
    books = load_books()
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    if title and author:
        new_book = {
            'id': str(len(books) + 1),
            'title': title,
            'author': author,
            'year': data.get('year'),
            'done': False
        }
        books.append(new_book)
        save_books(books)
        return jsonify(new_book), 201
    abort(400)

# Отримати окрему книгу за її ідентифікатором
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    books = load_books()
    book = next((book for book in books if book['id'] == str(book_id)), None)
    if book:
        return jsonify(book)
    abort(404)

# Видалити книгу за її ідентифікатором
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    books = load_books()
    index = next((index for index, book in enumerate(books) if book['id'] == str(book_id)), None)
    if index is not None:
        deleted_book = books.pop(index)
        save_books(books)
        return jsonify(deleted_book)
    abort(404)

# Оновити інформацію про книгу за її ідентифікатором
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    books = load_books()
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    done = data.get('done', False)
    book = next((book for book in books if book['id'] == str(book_id)), None)
    if book:
        book['title'] = title if title else book['title']
        book['author'] = author if author else book['author']
        book['year'] = data.get('year', book['year'])
        book['done'] = done
        save_books(books)
        return jsonify(book)
    abort(404)

# Головна сторінка
@app.route('/')
def home():
    return render_template('books.html')

if __name__ == "__main__":
    app.run(debug=True)
