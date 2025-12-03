"""
Book routes blueprint.
Handles all CRUD operations for books.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.book import db, Book
from datetime import datetime

# Create blueprint
book_bp = Blueprint('books', __name__)

@book_bp.route('/')
def index():
    """
    Homepage - Display all books.
    READ operation: Retrieves all books from database.
    """
    try:
        books = Book.query.order_by(Book.created_at.desc()).all()
        return render_template('index.html', books=books)
    except Exception as e:
        flash(f'Error loading books: {str(e)}', 'danger')
        return render_template('index.html', books=[])

@book_bp.route('/add', methods=['GET', 'POST'])
def add_book():
    """
    Add new book page.
    CREATE operation: Adds a new book to database.
    """
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title', '').strip()
            author = request.form.get('author', '').strip()
            genre = request.form.get('genre', '').strip()
            year_published = request.form.get('year_published', '').strip()
            description = request.form.get('description', '').strip()
            
            # Validate required fields
            if not all([title, author, genre, year_published]):
                flash('All fields except description are required!', 'warning')
                return render_template('add_book.html')
            
            # Validate year
            try:
                year_published = int(year_published)
                if year_published < 0 or year_published > datetime.now().year + 1:
                    flash('Please enter a valid year!', 'warning')
                    return render_template('add_book.html')
            except ValueError:
                flash('Year must be a valid number!', 'warning')
                return render_template('add_book.html')
            
            # Create new book
            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                year_published=year_published,
                description=description if description else None
            )
            
            # Add to database
            db.session.add(new_book)
            db.session.commit()
            
            flash(f'Book "{title}" added successfully!', 'success')
            return redirect(url_for('books.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding book: {str(e)}', 'danger')
            return render_template('add_book.html')
    
    # GET request - show form
    return render_template('add_book.html')

@book_bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    """
    Edit book page.
    UPDATE operation: Updates an existing book in database.
    """
    # Get the book from database
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form.get('title', '').strip()
            author = request.form.get('author', '').strip()
            genre = request.form.get('genre', '').strip()
            year_published = request.form.get('year_published', '').strip()
            description = request.form.get('description', '').strip()
            
            # Validate required fields
            if not all([title, author, genre, year_published]):
                flash('All fields except description are required!', 'warning')
                return render_template('edit_book.html', book=book)
            
            # Validate year
            try:
                year_published = int(year_published)
                if year_published < 0 or year_published > datetime.now().year + 1:
                    flash('Please enter a valid year!', 'warning')
                    return render_template('edit_book.html', book=book)
            except ValueError:
                flash('Year must be a valid number!', 'warning')
                return render_template('edit_book.html', book=book)
            
            # Update book fields
            book.title = title
            book.author = author
            book.genre = genre
            book.year_published = year_published
            book.description = description if description else None
            book.updated_at = datetime.utcnow()
            
            # Commit changes
            db.session.commit()
            
            flash(f'Book "{title}" updated successfully!', 'success')
            return redirect(url_for('books.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating book: {str(e)}', 'danger')
            return render_template('edit_book.html', book=book)
    
    # GET request - show form with pre-filled data
    return render_template('edit_book.html', book=book)

@book_bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    """
    Delete book.
    DELETE operation: Removes a book from database.
    Uses POST method for security (no GET deletes).
    """
    try:
        # Get the book
        book = Book.query.get_or_404(book_id)
        book_title = book.title
        
        # Delete from database
        db.session.delete(book)
        db.session.commit()
        
        flash(f'Book "{book_title}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting book: {str(e)}', 'danger')
    
    return redirect(url_for('books.index'))
