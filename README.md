# Library Management & Book Tracking System

A web-based application for managing library operations across EduLib Schools Consortium.

## Features

- **Book Management**: Add, edit, delete books with ISBN, title, author, genre, and quantity tracking.
- **Student Management**: Register students with personal and school information.
- **Borrowing & Returning**: Track book loans with automatic due dates and overdue detection.
- **Reporting**: Generate reports on most borrowed books, overdue items, and books per school.
- **User Interface**: Clean, Bootstrap-based web interface suitable for non-technical users.
- **REST API (for testing)**: A lightweight JSON API is available under `/api` for books, students, borrowings and statistics.

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

5. Initialize database (run migrations):
   ```powershell
   set FLASK_APP=run.py; flask db init; flask db migrate -m "initial"; flask db upgrade
   ```

6. Run the application:
   ```powershell
   python run.py
   ```

   Access the app at `http://localhost:5000`

## REST API (Testing)

For development/testing there is a simple JSON API registered under the blueprint `api` and available at `/api`.

Important: The API was made public (no authentication) for testing purposes — do not leave it public in production.

Available endpoints (examples):

- Books
  - `GET /api/books` — list books (query params: `available_only=true`, `genre=...`)
  - `GET /api/books/<id>` — get book details
  - `POST /api/books` — create book (JSON body: `isbn`, `title`, `author`, `quantity`, optional `genre`)
  - `PUT /api/books/<id>` — update book
  - `DELETE /api/books/<id>` — delete book

- Students
  - `GET /api/students` — list students
  - `GET /api/students/<id>` — student details
  - `POST /api/students` — create student (`email`, `full_name`, `class_name`, `school`)
  - `PUT /api/students/<id>` — update
  - `DELETE /api/students/<id>` — delete

- Borrowings
  - `GET /api/borrowings` — list borrowings (query params: `status`, `student_id`, `book_id`)
  - `POST /api/borrowings` — create borrowing (`student_id`, `book_id`)
  - `POST /api/borrowings/<id>/return` — mark borrowing returned

- Statistics
  - `GET /api/statistics` — library stats (total books, copies, active borrowings, overdue, etc.)

### Quick curl examples (PowerShell)

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/books" -Method GET
$body = @{
  isbn = '978-0-123456-78-9'
  title = 'Test Book'
  author = 'Test Author'
  quantity = 5
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/books" -Method POST -Body $body -ContentType 'application/json'
```

### Using Postman or Thunder Client

- Postman: create requests to `http://localhost:5000/api/...` and inspect responses.
- Thunder Client (VS Code extension): test endpoints directly inside VS Code.

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

## Notes & Cautions

- The API endpoints are currently public for testing. Before deploying to production, re-enable authentication on the API (restore `@login_required` / admin checks) and secure the app.
- The API blueprint is defined in `app/api.py` and registered in `app/__init__.py`.

## SDLC Documentation (Waterfall Model)

### 1. Requirements Analysis
- Functional requirements: Book CRUD, Student CRUD, Borrowing/Returning, Reporting
- Non-functional: Easy UI, SQLite database, Python/Flask backend

### 2. System Design
- Database schema: Books, Students, Borrowings tables
- Architecture: Flask MVC with templates

### 3. Implementation
- Code structure: `app/` with `models.py`, `routes.py`, `forms.py`, `templates/` and `api.py`

### 4. Testing
- Unit tests for models and key functions
- Manual testing via web UI and API

### 5. Deployment
- Switch to PostgreSQL for production, secure API, and configure proper secret keys and deploy behind HTTPS

## Future Enhancements
- Google Books API integration for auto-filling book details
- Email notifications for overdue books
- Barcode scanning for books
