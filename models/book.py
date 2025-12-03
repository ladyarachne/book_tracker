"""
Book model for SQLAlchemy ORM.
Represents the books table in the database.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class Book(db.Model):
    """
    Book model with all required fields.
    
    Attributes:
        id: Primary key
        title: Book title
        author: Book author
        genre: Book genre
        year_published: Year the book was published
        description: Book description
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """String representation of the Book object."""
        return f'<Book {self.title} by {self.author}>'
    
    def to_dict(self):
        """Convert Book object to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'year_published': self.year_published,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
