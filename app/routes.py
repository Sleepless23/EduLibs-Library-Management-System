from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from . import db
from .models import Book, Student, Borrowing
from .forms import BookForm, StudentForm, BorrowForm, LoginForm, SignupForm
from datetime import datetime

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. This is for administrators only.')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and student.check_password(form.password.data):
            login_user(student)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = SignupForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student:
            flash('Email already registered')
            return redirect(url_for('main.signup'))
        student = Student(
            email=form.email.data,
            full_name=form.full_name.data,
            class_name=form.class_name.data,
            school=form.school.data,
            contact=form.contact.data
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Account created successfully! Please log in.')
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        # Admin dashboard with statistics
        total_books = Book.query.count()
        available_books_count = Book.query.filter(Book.available_quantity > 0).count()
        total_students = Student.query.count()
        active_borrowings = Borrowing.query.filter(Borrowing.status == 'borrowed').count()
        overdue_books = Borrowing.query.filter(Borrowing.status == 'borrowed', Borrowing.due_date < datetime.utcnow()).count()

        # Recent borrowings
        recent_borrowings = Borrowing.query.order_by(Borrowing.borrow_date.desc()).limit(10).all()

        return render_template('admin_dashboard.html',
                               total_books=total_books,
                               available_books_count=available_books_count,
                               total_students=total_students,
                               active_borrowings=active_borrowings,
                               overdue_books=overdue_books,
                               recent_borrowings=recent_borrowings)

    # Student dashboard
    # Available books
    available_books = Book.query.filter(Book.available_quantity > 0).all()

    # Currently borrowed books
    borrowed_books = [b.book for b in current_user.borrowings if b.status == 'borrowed']

    # Borrowing history
    history = [b for b in current_user.borrowings if b.status == 'returned']

    from sqlalchemy import func
    popular_books = db.session.query(Book, func.count(Borrowing.id).label('borrow_count')) \
        .join(Borrowing).group_by(Book.id).order_by(func.count(Borrowing.id).desc()).limit(5).all()
    recommendations = [book for book, _ in popular_books]

    return render_template('student_dashboard.html',
                          available_books=available_books,
                          borrowed_books=borrowed_books,
                          history=history,
                          recommendations=recommendations)

@bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_quantity > 0:
        borrowing = Borrowing(student_id=current_user.id, book_id=book_id)
        book.available_quantity -= 1
        db.session.add(borrowing)
        db.session.commit()
        flash('Book borrowed successfully!')
    else:
        flash('Book is not available.')
    return redirect(url_for('main.dashboard'))

@bp.route('/return/<int:borrowing_id>', methods=['POST'])
@login_required
def return_borrowing(borrowing_id):
    borrowing = Borrowing.query.get_or_404(borrowing_id)
    if borrowing.student_id == current_user.id and borrowing.status == 'borrowed':
        borrowing.return_date = datetime.utcnow()
        borrowing.status = 'returned'
        borrowing.book.available_quantity += 1
        db.session.commit()
        flash('Book returned successfully!')
    else:
        flash('Unable to return book.')
    return redirect(url_for('main.dashboard'))


#book route
@bp.route('/books')
@admin_required
def books():
    books = Book.query.all()
    total_books = len(books)
    available_titles = sum(1 for book in books if book.available_quantity > 0)
    total_copies = sum(book.quantity for book in books)
    return render_template('books.html', books=books, total_books=total_books, 
                         available_titles=available_titles, total_copies=total_copies)

@bp.route('/books/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        # Check if ISBN already exists
        existing_book = Book.query.filter_by(isbn=form.isbn.data).first()
        if existing_book:
            flash('A book with this ISBN already exists.')
            return render_template('add_book.html', form=form)

        book = Book(
            isbn=form.isbn.data,
            title=form.title.data,
            author=form.author.data,
            genre=form.genre.data,
            quantity=form.quantity.data,
            available_quantity=form.quantity.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('main.books'))
    return render_template('add_book.html', form=form)

@bp.route('/books/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        borrowed_count = len([b for b in book.borrowings if b.status == 'borrowed'])
        book.available_quantity = book.quantity - borrowed_count
        db.session.commit()
        flash('Book updated successfully!')
        return redirect(url_for('main.books'))
    return render_template('edit_book.html', form=form)

@bp.route('/books/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    return redirect(url_for('main.books'))

#avail books
@bp.route('/available_books')
@login_required
def available_books():
    genre = request.args.get('genre')
    search = request.args.get('search')
    sort_by = request.args.get('sort', 'title')

    query = Book.query.filter(Book.available_quantity > 0)

    if genre:
        query = query.filter(Book.genre == genre)

    if search:
        query = query.filter(
            db.or_(
                Book.title.contains(search),
                Book.author.contains(search)
            )
        )

    if sort_by == 'genre':
        query = query.order_by(Book.genre, Book.title)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    # Get all available genres
    genres = db.session.query(Book.genre).filter(Book.available_quantity > 0).distinct().order_by(Book.genre).all()
    genres = [g[0] for g in genres]

    return render_template('available_books.html', books=books, genres=genres, selected_genre=genre, search=search, sort_by=sort_by)

@bp.route('/my_books')
@login_required
def my_books():
    borrowed_books = [b.book for b in current_user.borrowings if b.status == 'borrowed']
    borrowings = {b.book_id: b for b in current_user.borrowings if b.status == 'borrowed'}
    return render_template('my_books.html', borrowed_books=borrowed_books, borrowings=borrowings)

@bp.route('/borrowing_history')
@login_required
def borrowing_history():
    history = [b for b in current_user.borrowings if b.status == 'returned']
    return render_template('borrowing_history.html', history=history)


#stud route
@bp.route('/students')
@admin_required
def students():
    students = Student.query.all()
    total_current = 0
    total_all = 0
    for student in students:
        student.current_borrowed = len([b for b in student.borrowings if b.status == 'borrowed'])
        student.total_borrowed = len(student.borrowings)
        total_current += student.current_borrowed
        total_all += student.total_borrowed
    return render_template('students.html', students=students, total_current=total_current, total_all=total_all)

@bp.route('/students/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            full_name=form.full_name.data,
            class_name=form.class_name.data,
            school=form.school.data,
            contact=form.contact.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!')
        return redirect(url_for('main.students'))
    return render_template('add_student.html', form=form)

@bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('Student updated successfully!')
        return redirect(url_for('main.students'))
    return render_template('edit_student.html', form=form)

@bp.route('/students/delete/<int:id>')
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    if student.is_admin:
        flash('Cannot delete admin user!')
        return redirect(url_for('main.students'))

    # Check if student has active borrowings
    active_borrowings = [b for b in student.borrowings if b.status == 'borrowed']
    if active_borrowings:
        flash(f'Cannot delete student with {len(active_borrowings)} active borrowing(s). Please return all books first.')
        return redirect(url_for('main.students'))

    # Delete
    Borrowing.query.filter_by(student_id=id).delete()
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!')
    return redirect(url_for('main.students'))


# borrow routes
@bp.route('/borrow', methods=['GET', 'POST'])
@admin_required
def borrow():
    from datetime import datetime
    total_borrowings = Borrowing.query.count()
    available_books_count = Book.query.filter(Book.available_quantity > 0).count()
    active_borrowings = Borrowing.query.filter(Borrowing.status == 'borrowed').count()
    overdue_books = Borrowing.query.filter(Borrowing.status == 'borrowed', Borrowing.due_date < datetime.utcnow()).count()

    form = BorrowForm()
    form.student_id.choices = [(s.id, s.full_name) for s in Student.query.all()]
    form.book_id.choices = [(b.id, f"{b.title} ({b.available_quantity} available)") for b in Book.query.filter(Book.available_quantity > 0).all()]
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        if book.available_quantity > 0:
            borrowing = Borrowing(student_id=form.student_id.data, book_id=form.book_id.data)
            book.available_quantity -= 1
            db.session.add(borrowing)
            db.session.commit()
            flash('Book borrowed successfully!')
            return redirect(url_for('main.borrowings'))
        else:
            flash('No copies available!')
    return render_template('borrow.html',
                         form=form,
                         total_borrowings=total_borrowings,
                         available_books_count=available_books_count,
                         active_borrowings=active_borrowings,
                         overdue_books=overdue_books)

@bp.route('/borrowings')
@admin_required
def borrowings():
    from datetime import datetime
    # Order borrowings newest first so latest entries appear at the top
    borrowings = Borrowing.query.order_by(Borrowing.borrow_date.desc()).all()
    current_time = datetime.utcnow()

    # Calculate statistics
    total_borrowings = len(borrowings)
    active_count = sum(1 for b in borrowings if b.status == 'borrowed')
    overdue_count = sum(1 for b in borrowings if b.status == 'borrowed' and b.due_date < current_time)
    returned_count = sum(1 for b in borrowings if b.status == 'returned')

    return render_template('borrowings.html',
                         borrowings=borrowings,
                         current_time=current_time,
                         total_borrowings=total_borrowings,
                         active_count=active_count,
                         overdue_count=overdue_count,
                         returned_count=returned_count)

@bp.route('/reports')
@admin_required
def reports():
    from sqlalchemy import func
    from datetime import datetime

    count_col = func.count(Borrowing.id).label('borrow_count')
    most_borrowed = db.session.query(Book.title, count_col).join(Borrowing).group_by(Book.id).order_by(count_col.desc()).limit(10).all()
    overdue = Borrowing.query.filter(Borrowing.due_date < datetime.utcnow(), Borrowing.status == 'borrowed').all()
    books_per_school = db.session.query(Student.school, func.count(Borrowing.id)).join(Borrowing).group_by(Student.school).all()

    return render_template('reports.html', most_borrowed=most_borrowed, overdue=overdue, books_per_school=books_per_school)

@bp.route('/return/<int:id>', methods=['POST'])
@login_required
def return_book(id):
    try:
        # Only allow admins to perform a return, but allow the route to run for logged-in users
        if not getattr(current_user, 'is_admin', False):
            flash('Access denied. Only administrators may mark returns.')
            return redirect(url_for('main.borrowings'))

        borrowing = Borrowing.query.get_or_404(id)
        borrowing.return_date = datetime.utcnow()
        borrowing.status = 'returned'
        borrowing.book.available_quantity += 1
        db.session.commit()
        flash('Book returned successfully!')
    except Exception as e:
        print(f"ERROR returning book: {str(e)}")  # Print to console for debugging
        db.session.rollback()
        flash(f'Failed to mark book as returned: {str(e)}')
    return redirect(url_for('main.borrowings'))

# export route
@bp.route('/export/popular-books/csv')
@admin_required
def export_popular_books_csv():
    from sqlalchemy import func
    import pandas as pd
    from flask import Response
    import io

    # Get most borrowed books data
    most_borrowed = db.session.query(Book.title, func.count(Borrowing.id).label('borrow_count')) \
        .join(Borrowing).group_by(Book.id).order_by(func.count(Borrowing.id).desc()).all()

    df = pd.DataFrame(most_borrowed, columns=['Book Title', 'Borrow Count'])

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=popular_books_report.csv'}
    )

    return response

@bp.route('/export/school-books/csv')
@admin_required
def export_school_books_csv():
    from sqlalchemy import func
    import pandas as pd
    from flask import Response
    import io

    # Get books per school data
    books_per_school = db.session.query(Student.school, func.count(Borrowing.id)).join(Borrowing).group_by(Student.school).all()

    # Convert to DataFrame
    df = pd.DataFrame(books_per_school, columns=['School', 'Total Borrows'])

    # Create CSV in memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Create response
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=school_books_report.csv'}
    )

    return response

@bp.route('/export/borrowings/csv')
@admin_required
def export_borrowings_csv():
    import pandas as pd
    from flask import Response
    import io

    # Get all borrowings data
    borrowings = Borrowing.query.all()
    borrowings_data = []

    for borrowing in borrowings:
        borrowings_data.append({
            'Student Name': borrowing.student.full_name,
            'Book Title': borrowing.book.title,
            'ISBN': borrowing.book.isbn,
            'Borrow Date': borrowing.borrow_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Due Date': borrowing.due_date.strftime('%Y-%m-%d'),
            'Return Date': borrowing.return_date.strftime('%Y-%m-%d %H:%M:%S') if borrowing.return_date else 'Not Returned',
            'Status': borrowing.status.title(),
            'School': borrowing.student.school
        })

    df = pd.DataFrame(borrowings_data)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=all_borrowings_report.csv'}
    )

    return response

#open lib api
@bp.route('/search-books')
@login_required
def search_books():
    query = request.args.get('q', '')
    results = []

    if query:
        try:
            import requests
            response = requests.get(f'https://openlibrary.org/search.json?q={query}&limit=20')
            if response.status_code == 200:
                data = response.json()
                results = []
                for doc in data.get('docs', []):
                    book_info = {
                        'title': doc.get('title', 'Unknown Title'),
                        'author': ', '.join(doc.get('author_name', ['Unknown Author'])),
                        'isbn': doc.get('isbn', [None])[0] if doc.get('isbn') else None,
                        'publish_year': doc.get('first_publish_year', 'Unknown'),
                        'publisher': ', '.join(doc.get('publisher', ['Unknown'])) if doc.get('publisher') else 'Unknown',
                        'cover_url': None,
                        'key': doc.get('key', ''),
                        'genre': doc.get('subject', [''])[0] if doc.get('subject') else 'Unknown'
                    }
                    if doc.get('cover_i'):
                        book_info['cover_url'] = f"https://covers.openlibrary.org/b/id/{doc['cover_i']}-M.jpg"

                    results.append(book_info)
        except Exception as e:
            flash(f'Error searching books: {str(e)}', 'error')

    return render_template('search_books.html', query=query, results=results)

@bp.route('/import-book/<path:openlibrary_key>', methods=['POST'])
@admin_required
def import_book(openlibrary_key):
    try:
        import requests
        response = requests.get(f'https://openlibrary.org{openlibrary_key}.json')
        if response.status_code == 200:
            data = response.json()

            # Extract book information
            title = data.get('title', 'Unknown Title')
            authors = data.get('authors', [])
            author_names = []

            # Get author names
            for author_ref in authors:
                if isinstance(author_ref, dict) and 'key' in author_ref:
                    author_response = requests.get(f"https://openlibrary.org{author_ref['key']}.json")
                    if author_response.status_code == 200:
                        author_data = author_response.json()
                        author_names.append(author_data.get('name', 'Unknown Author'))

            author = ', '.join(author_names) if author_names else 'Unknown Author'

            # Get ISBN
            isbns = data.get('isbn_13', []) + data.get('isbn_10', [])
            isbn = isbns[0] if isbns else None

            # Get genre/subject
            subjects = data.get('subjects', [])
            genre = subjects[0] if subjects else 'Unknown'

            # Get publish year
            publish_date = data.get('publish_date', 'Unknown')

            # Check if book already exists
            existing_book = Book.query.filter_by(title=title, author=author).first()
            if existing_book:
                flash('This book already exists in the library.', 'warning')
                return redirect(url_for('main.search_books'))
            

            # Create new book
            new_book = Book(
                isbn=isbn,
                title=title,
                author=author,
                genre=genre,
                quantity=1, 
                available_quantity=1
            )

            db.session.add(new_book)
            db.session.commit()

            flash(f'Successfully imported "{title}" to the library!', 'success')
        else:
            flash('Failed to retrieve book details from Open Library.', 'error')
    except Exception as e:
        flash(f'Error importing book: {str(e)}', 'error')

    return redirect(url_for('main.search_books'))