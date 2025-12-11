from app import create_app, db
from app.models import Book, Student, Borrowing

def populate_db():
    app = create_app()
    with app.app_context():
        Borrowing.query.delete()
        old_students = Student.query.filter(Student.email.in_(['alice@email.com', 'bob@email.com', 'carol@email.com'])).all()
        for student in old_students:
            db.session.delete(student)
        db.session.commit()
        
        books = [
            Book(isbn='9780061120084', title='To Kill a Mockingbird', author='Harper Lee', genre='Fiction', quantity=4),
            Book(isbn='9780451524935', title='1984', author='George Orwell', genre='Dystopian', quantity=3),
            Book(isbn='9780743273565', title='The Great Gatsby', author='F. Scott Fitzgerald', genre='Classic', quantity=3),
            Book(isbn='9780141439518', title='Pride and Prejudice', author='Jane Austen', genre='Romance', quantity=5),
            Book(isbn='9780547928227', title='The Hobbit', author='J.R.R. Tolkien', genre='Fantasy', quantity=4),
            Book(isbn='9780439708180', title='Harry Potter and the Sorcerer\'s Stone', author='J.K. Rowling', genre='Fantasy', quantity=5),
            Book(isbn='9780307474278', title='The Da Vinci Code', author='Dan Brown', genre='Thriller', quantity=3),
            Book(isbn='9780062315007', title='The Alchemist', author='Paulo Coelho', genre='Adventure', quantity=4),
            Book(isbn='9780439023481', title='The Hunger Games', author='Suzanne Collins', genre='Dystopian', quantity=5),
            Book(isbn='9781503280786', title='Moby Dick', author='Herman Melville', genre='Classic', quantity=2),
            Book(isbn='9780060850524', title='Brave New World', author='Aldous Huxley', genre='Dystopian', quantity=4),
            Book(isbn='9780525478812', title='The Fault in Our Stars', author='John Green', genre='Romance', quantity=3),
            Book(isbn='9780307949486', title='The Girl with the Dragon Tattoo', author='Stieg Larsson', genre='Mystery', quantity=3),
            Book(isbn='9780553103540', title='A Game of Thrones', author='George R.R. Martin', genre='Fantasy', quantity=4),
            Book(isbn='9780262033848', title='Introduction to Algorithms', author='Thomas H. Cormen', genre='Academic', quantity=2),
            Book(isbn='9780073383095', title='Discrete Mathematics and Its Applications', author='Kenneth H. Rosen', genre='Academic', quantity=3),
            Book(isbn='9780136042594', title='Artificial Intelligence: A Modern Approach', author='Stuart Russell, Peter Norvig', genre='Academic', quantity=2),
            Book(isbn='9780030105678', title='Linear Algebra and Its Applications', author='Gilbert Strang', genre='Academic', quantity=3),
            Book(isbn='9780073523323', title='Database System Concepts', author='Abraham Silberschatz', genre='Academic', quantity=4),
            Book(isbn='9780534493394', title='Physics for Scientists and Engineers', author='Raymond A. Serway', genre='Academic', quantity=3),
            Book(isbn='9789712730012', title='ABNKKBSNPLAko?!', author='Bob Ong', genre='Filipino / Humor', quantity=5),
            Book(isbn='9789712730023', title='Macarthur', author='Bob Ong', genre='Filipino / Humor', quantity=4),
            Book(isbn='9789712730034', title='Si', author='Bob Ong', genre='Filipino / Fiction', quantity=3),
            Book(isbn='9789712730045', title='Alamat ng Gubat', author='Bob Ong', genre='Filipino / Children', quantity=5),
            Book(isbn='9789712730056', title='Wattpad: Diary ng Panget', author='HaveYouSeenThisGirl', genre='Wattpad / Romance', quantity=4),
            Book(isbn='9789712730067', title='She\'s Dating the Gangster', author='Bianca Bernardino', genre='Wattpad / Romance', quantity=5),
            Book(isbn='9789712730078', title='The Bet', author='Marina', genre='Wattpad / Romance', quantity=3),
            Book(isbn='9789712730089', title='My Life with the Walter Boys', author='Ali Novak', genre='Wattpad / Romance', quantity=4),
            Book(isbn='9789712730090', title='Filipino Heroes: Katipunan Stories', author='National Authors', genre='Filipino / History', quantity=2),
            Book(isbn='9789712730101', title='Mga Ibong Mandaragit', author='Amado V. Hernandez', genre='Filipino / Classic', quantity=3),
            Book(isbn='9789712730112', title='Dekada \'70', author='Lualhati Bautista', genre='Filipino / Fiction / Historical', quantity=4),
            Book(isbn='9789712730123', title='Gapô', author='Lualhati Bautista', genre='Filipino / Fiction / Social Commentary', quantity=3),
            Book(isbn='9789712730134', title='Bata, Bata… Pa\'no Ka Ginawa?', author='Lualhati Bautista', genre='Filipino / Fiction', quantity=4),
        ]

        for book in books:
            existing = Book.query.filter_by(isbn=book.isbn).first()
            if not existing:
                book.available_quantity = book.quantity
                db.session.add(book)
        students = [
            Student(email='admin@edulib.com', full_name='Admin User', class_name='N/A', school='EduLib', contact='admin@edulib.com', is_admin=True),
        ]

        for student in students:
            existing = Student.query.filter_by(email=student.email).first()
            if not existing:
                if student.email == 'admin@edulib.com':
                    student.set_password('admin123')
                else:
                    student.set_password('password123')  
                db.session.add(student)
            else:
                
                if student.email == 'admin@edulib.com':
                    existing.set_password('admin123')
                else:
                    existing.set_password('password123')
        from datetime import datetime, timedelta
        import random

        # Commit the student/borrowing data
        db.session.commit()

        active_count = Borrowing.query.filter(Borrowing.status == 'borrowed').count()
        overdue_count = Borrowing.query.filter(Borrowing.due_date < datetime.utcnow(), Borrowing.status == 'borrowed').count()
        total_books = Book.query.count()
        available_books = Book.query.filter(Book.available_quantity > 0).count()

        print("Sample data added successfully!")
        print(f"Total books: {total_books}")
        print(f"Available books: {available_books}")
        print(f"Active borrowings: {active_count}")
        print(f"Overdue borrowings: {overdue_count}")

if __name__ == '__main__':
    populate_db()