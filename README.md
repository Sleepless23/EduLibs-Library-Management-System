# EduLibs-Library-Management-System-3A

Library Management & Book Tracking System — Client Problem Statement
Client Information

Client Name: Henry Moreno
Position: Operations Manager
Organization: EduLib Schools Consortium
Type: Private School Network (14 schools)

📌 Background

EduLib Schools Consortium currently manages library records using Excel sheets and handwritten logbooks. This has resulted in missing books, inconsistent records, and difficulties tracking which school holds which materials.

The organization wants to transition to a centralized digital library system that is easy for librarians—many of whom have limited ICT skills—to use effectively.

🔥 Current Problems

All library records (books, borrowers, returns) are stored in paper files or Excel, causing frequent data loss and errors.

Books are often lost or unreturned, with no automated overdue tracking.

New book entries are typed manually, resulting in wrong titles, authors, and genres.

Administrators cannot easily generate reports such as:

Most borrowed books

Books per school

Overdue books

No standardized system across the 14 school libraries.

🎯 Project Goal

To build a simple, reliable Library Management & Book Tracking System that improves accountability, reduces book loss, and standardizes library operations across all EduLib schools.

🖥️ System Requirements
✔ 1. Book Management

Add new books

Edit book details

Delete books

Store ISBN, title, author, genre, and quantity

(Optional) Automatically fill book details using the Google Books API when ISBN is entered

✔ 2. Student Management

Register students with:

Full name

Class

School

Contact information

✔ 3. Borrowing & Returning

Record when a student borrows a book

Auto-generate due dates

Track overdue books

Mark books as returned

Prevent borrowing if no copies are available

✔ 4. Reporting

System should generate useful reports such as:

Most Borrowed Books Report

Overdue Books List

Total Books per School

Borrowing History per Student

Reports should be exportable as PDF or CSV.

✔ 5. User Experience Requirements

System must be clean and easy for non-technical librarians

Clear menus and instructions

Must work even with slow internet or offline (depending on solution type)

🛠️ Technical Requirements

Python-based backend

Optional Flask web interface or CLI interface

SQLite or PostgreSQL database

Git (feature-branch workflow)

Proper SDLC documentation following the Waterfall Model

Unit tests for key features (book creation, borrowing, etc.)
