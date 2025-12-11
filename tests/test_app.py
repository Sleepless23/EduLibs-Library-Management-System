import unittest
from app import create_app, db
from app.models import Book, Student, Borrowing
from datetime import datetime, timedelta

class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_book_creation(self):
        with self.app.app_context():
            book = Book(isbn='1234567890', title='Test Book', author='Test Author', genre='Fiction', quantity=5)
            db.session.add(book)
            db.session.commit()
            self.assertEqual(book.available_quantity, 5)

    def test_student_creation(self):
        with self.app.app_context():
            student = Student(full_name='John Doe', class_name='10A', school='School A', contact='john@example.com')
            db.session.add(student)
            db.session.commit()
            self.assertEqual(student.full_name, 'John Doe')

    def test_borrowing(self):
        with self.app.app_context():
            book = Book(isbn='1234567890', title='Test Book', author='Test Author', quantity=1)
            student = Student(full_name='John Doe', class_name='10A', school='School A')
            db.session.add(book)
            db.session.add(student)
            db.session.commit()

            borrowing = Borrowing(student_id=student.id, book_id=book.id)
            db.session.add(borrowing)
            db.session.commit()

            self.assertEqual(book.available_quantity, 0)
            self.assertEqual(borrowing.status, 'borrowed')

    def test_returning(self):
        with self.app.app_context():
            book = Book(isbn='1234567890', title='Test Book', author='Test Author', quantity=1)
            student = Student(full_name='John Doe', class_name='10A', school='School A')
            db.session.add(book)
            db.session.add(student)
            db.session.commit()

            borrowing = Borrowing(student_id=student.id, book_id=book.id)
            db.session.add(borrowing)
            db.session.commit()

            # Return
            borrowing.return_date = datetime.utcnow()
            borrowing.status = 'returned'
            book.available_quantity += 1
            db.session.commit()

            self.assertEqual(book.available_quantity, 1)
            self.assertEqual(borrowing.status, 'returned')

if __name__ == '__main__':
    unittest.main()