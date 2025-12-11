from app import create_app

app = create_app()

if __name__ == '__main__':
    from populate_db import populate_db
    
    # Only populate if database is empty (first run)
    with app.app_context():
        from app.models import Book, Student
        if Book.query.first() is None and Student.query.first() is None:
            print("Database empty. Populating sample data...")
            populate_db()
        else:
            print("Database already populated. Skipping populate_db()...")

    app.run(debug=True)