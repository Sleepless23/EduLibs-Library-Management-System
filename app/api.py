from flask import Blueprint, jsonify, request
from functools import wraps
from . import db
from .models import Book, Student, Borrowing
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books with optional filtering"""
    try:
        available_only = request.args.get('available_only', 'false').lower() == 'true'
        genre = request.args.get('genre')
        
        query = Book.query
        
        if available_only:
            query = query.filter(Book.available_quantity > 0)
        
        if genre:
            query = query.filter(Book.genre == genre)
        
        books = query.all()
        
        return jsonify({
            'success': True,
            'count': len(books),
            'books': [
                {
                    'id': book.id,
                    'isbn': book.isbn,
                    'title': book.title,
                    'author': book.author,
                    'genre': book.genre,
                    'quantity': book.quantity,
                    'available_quantity': book.available_quantity
                }
                for book in books
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book by ID"""
    try:
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({
            'success': True,
            'book': {
                'id': book.id,
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'quantity': book.quantity,
                'available_quantity': book.available_quantity
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/books', methods=['POST'])
def create_book():
    """Create a new book"""
    try:
        data = request.get_json()
        

        required_fields = ['isbn', 'title', 'author', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        existing_book = Book.query.filter_by(isbn=data['isbn']).first()
        if existing_book:
            return jsonify({'error': 'A book with this ISBN already exists'}), 409
        
        book = Book(
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            genre=data.get('genre', ''),
            quantity=int(data['quantity']),
            available_quantity=int(data['quantity'])
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book created successfully',
            'book': {
                'id': book.id,
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'quantity': book.quantity,
                'available_quantity': book.available_quantity
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a book"""
    try:
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'genre' in data:
            book.genre = data['genre']
        if 'quantity' in data:
            book.quantity = int(data['quantity'])
        if 'available_quantity' in data:
            book.available_quantity = int(data['available_quantity'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book updated successfully',
            'book': {
                'id': book.id,
                'isbn': book.isbn,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'quantity': book.quantity,
                'available_quantity': book.available_quantity
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book"""
    try:
        book = Book.query.get(book_id)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        active_borrowings = Borrowing.query.filter(
            Borrowing.book_id == book_id,
            Borrowing.status == 'borrowed'
        ).count()
        
        if active_borrowings > 0:
            return jsonify({
                'error': 'Cannot delete book with active borrowings'
            }), 409
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@api_bp.route('/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        students = Student.query.all()
        
        return jsonify({
            'success': True,
            'count': len(students),
            'students': [
                {
                    'id': student.id,
                    'email': student.email,
                    'full_name': student.full_name,
                    'class_name': student.class_name,
                    'school': student.school,
                    'contact': student.contact,
                    'is_admin': student.is_admin
                }
                for student in students
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a specific student by ID"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        return jsonify({
            'success': True,
            'student': {
                'id': student.id,
                'email': student.email,
                'full_name': student.full_name,
                'class_name': student.class_name,
                'school': student.school,
                'contact': student.contact,
                'is_admin': student.is_admin
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/students', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'full_name', 'class_name', 'school']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        existing_student = Student.query.filter_by(email=data['email']).first()
        if existing_student:
            return jsonify({'error': 'A student with this email already exists'}), 409
        
        student = Student(
            email=data['email'],
            full_name=data['full_name'],
            class_name=data['class_name'],
            school=data['school'],
            contact=data.get('contact', ''),
            is_admin=False
        )
        
        db.session.add(student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'student': {
                'id': student.id,
                'email': student.email,
                'full_name': student.full_name,
                'class_name': student.class_name,
                'school': student.school,
                'contact': student.contact,
                'is_admin': student.is_admin
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
 
        if 'full_name' in data:
            student.full_name = data['full_name']
        if 'class_name' in data:
            student.class_name = data['class_name']
        if 'school' in data:
            student.school = data['school']
        if 'contact' in data:
            student.contact = data['contact']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully',
            'student': {
                'id': student.id,
                'email': student.email,
                'full_name': student.full_name,
                'class_name': student.class_name,
                'school': student.school,
                'contact': student.contact,
                'is_admin': student.is_admin
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student"""
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        active_borrowings = Borrowing.query.filter(
            Borrowing.student_id == student_id,
            Borrowing.status == 'borrowed'
        ).count()
        
        if active_borrowings > 0:
            return jsonify({
                'error': 'Cannot delete student with active borrowings'
            }), 409
        
        db.session.delete(student)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ==================== BORROWING ENDPOINTS ====================

@api_bp.route('/borrowings', methods=['GET'])
def get_borrowings():
    """Get all borrowings with optional filtering"""
    try:
        status = request.args.get('status')
        student_id = request.args.get('student_id', type=int)
        book_id = request.args.get('book_id', type=int)
        
        query = Borrowing.query
        
        if status:
            query = query.filter(Borrowing.status == status)
        if student_id:
            query = query.filter(Borrowing.student_id == student_id)
        if book_id:
            query = query.filter(Borrowing.book_id == book_id)
        
        borrowings = query.all()
        
        return jsonify({
            'success': True,
            'count': len(borrowings),
            'borrowings': [
                {
                    'id': borrowing.id,
                    'student_id': borrowing.student_id,
                    'student_name': borrowing.student.full_name,
                    'book_id': borrowing.book_id,
                    'book_title': borrowing.book.title,
                    'borrow_date': borrowing.borrow_date.isoformat(),
                    'due_date': borrowing.due_date.isoformat() if borrowing.due_date else None,
                    'return_date': borrowing.return_date.isoformat() if borrowing.return_date else None,
                    'status': borrowing.status
                }
                for borrowing in borrowings
            ]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/borrowings/<int:borrowing_id>', methods=['GET'])
def get_borrowing(borrowing_id):
    """Get a specific borrowing by ID"""
    try:
        borrowing = Borrowing.query.get(borrowing_id)
        
        if not borrowing:
            return jsonify({'error': 'Borrowing record not found'}), 404
        
        return jsonify({
            'success': True,
            'borrowing': {
                'id': borrowing.id,
                'student_id': borrowing.student_id,
                'student_name': borrowing.student.full_name,
                'book_id': borrowing.book_id,
                'book_title': borrowing.book.title,
                'borrow_date': borrowing.borrow_date.isoformat(),
                'due_date': borrowing.due_date.isoformat() if borrowing.due_date else None,
                'return_date': borrowing.return_date.isoformat() if borrowing.return_date else None,
                'status': borrowing.status
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/borrowings', methods=['POST'])
def create_borrowing():
    """Create a new borrowing record"""
    try:
        data = request.get_json()

        if 'student_id' not in data or 'book_id' not in data:
            return jsonify({'error': 'Missing required fields: student_id and book_id'}), 400
        
        student = Student.query.get(data['student_id'])
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        book = Book.query.get(data['book_id'])
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        if book.available_quantity <= 0:
            return jsonify({'error': 'No copies available for this book'}), 409
        
        borrowing = Borrowing(
            student_id=data['student_id'],
            book_id=data['book_id']
        )
        
        book.available_quantity -= 1
        db.session.add(borrowing)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Borrowing record created successfully',
            'borrowing': {
                'id': borrowing.id,
                'student_id': borrowing.student_id,
                'student_name': borrowing.student.full_name,
                'book_id': borrowing.book_id,
                'book_title': borrowing.book.title,
                'borrow_date': borrowing.borrow_date.isoformat(),
                'due_date': borrowing.due_date.isoformat() if borrowing.due_date else None,
                'return_date': borrowing.return_date.isoformat() if borrowing.return_date else None,
                'status': borrowing.status
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/borrowings/<int:borrowing_id>/return', methods=['POST'])
def return_book(borrowing_id):
    """Mark a book as returned"""
    try:
        borrowing = Borrowing.query.get(borrowing_id)
        
        if not borrowing:
            return jsonify({'error': 'Borrowing record not found'}), 404
        
        if borrowing.status == 'returned':
            return jsonify({'error': 'Book has already been returned'}), 409
        
        borrowing.status = 'returned'
        borrowing.return_date = datetime.utcnow()
        borrowing.book.available_quantity += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book returned successfully',
            'borrowing': {
                'id': borrowing.id,
                'student_id': borrowing.student_id,
                'student_name': borrowing.student.full_name,
                'book_id': borrowing.book_id,
                'book_title': borrowing.book.title,
                'borrow_date': borrowing.borrow_date.isoformat(),
                'due_date': borrowing.due_date.isoformat() if borrowing.due_date else None,
                'return_date': borrowing.return_date.isoformat() if borrowing.return_date else None,
                'status': borrowing.status
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/borrowings/<int:borrowing_id>', methods=['DELETE'])
def delete_borrowing(borrowing_id):
    """Delete a borrowing record"""
    try:
        borrowing = Borrowing.query.get(borrowing_id)
        
        if not borrowing:
            return jsonify({'error': 'Borrowing record not found'}), 404
        
        if borrowing.status == 'borrowed':
            borrowing.book.available_quantity += 1
        
        db.session.delete(borrowing)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Borrowing record deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get library statistics"""
    try:
        total_books = Book.query.count()
        total_copies = sum(book.quantity for book in Book.query.all()) or 0
        available_books = Book.query.filter(Book.available_quantity > 0).count()
        total_students = Student.query.count()
        active_borrowings = Borrowing.query.filter(Borrowing.status == 'borrowed').count()
        overdue_books = Borrowing.query.filter(
            Borrowing.status == 'borrowed',
            Borrowing.due_date < datetime.utcnow()
        ).count()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_books': total_books,
                'total_copies': total_copies,
                'available_books': available_books,
                'total_students': total_students,
                'active_borrowings': active_borrowings,
                'overdue_books': overdue_books
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500