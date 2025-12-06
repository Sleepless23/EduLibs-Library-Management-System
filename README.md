# Library Management & Book Tracking System

A web-based application for managing library operations across EduLib Schools Consortium.

## Features

- **Book Management**: Add, edit, delete books with ISBN, title, author, genre, and quantity tracking.
- **Student Management**: Register students with personal and school information.
- **Borrowing & Returning**: Track book loans with automatic due dates and overdue detection.
- **Reporting**: Generate reports on most borrowed books, overdue items, and books per school.
- **User Interface**: Clean, Bootstrap-based web interface suitable for non-technical users.

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily switchable to PostgreSQL)
- **Frontend**: HTML, CSS (Bootstrap), Jinja2 templates
- **Forms**: Flask-WTF
- **Migrations**: Flask-Migrate

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd library_management_system
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize database:
   ```bash
   set FLASK_APP=run.py
   flask db init
   flask db migrate -m "initial"
   flask db upgrade
   ```

6. Run the application:
   ```bash
   python run.py
   ```

   Access at http://localhost:5000

## Usage

- Navigate to the home page and use the menu to manage books, students, borrowings, and view reports.
- Add books by providing ISBN, title, author, etc.
- Register students with their details.
- Borrow books by selecting student and available book.
- Return books from the borrowings list.
- View reports for insights into library usage.

## Testing

Run unit tests:
```bash
python -m unittest tests/test_app.py
```

## SDLC Documentation (Waterfall Model)

### 1. Requirements Analysis
- Functional requirements: Book CRUD, Student CRUD, Borrowing/Returning, Reporting
- Non-functional: Easy UI, SQLite database, Python/Flask backend
- User stories from client problem statement

### 2. System Design
- Database schema: Books, Students, Borrowings tables
- Architecture: Flask MVC with templates
- UI wireframes: Simple forms and tables

### 3. Implementation
- Code structure: app/ with models, routes, forms, templates
- Features implemented as per requirements

### 4. Testing
- Unit tests for models and key functions
- Manual testing of web interface

### 5. Deployment
- Instructions for setup and running
- Production considerations: Switch to PostgreSQL, add authentication if needed

## Future Enhancements

- User authentication for librarians
- Google Books API integration for auto-filling book details
- PDF/CSV export for reports
- Email notifications for overdue books
- Barcode scanning for books

## License

This project is for EduLib Schools Consortium.