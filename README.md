# 📚 Book Tracker - Flask Web Application

A complete CRUD (Create, Read, Update, Delete) web application for tracking your book collection, built with Flask, SQLAlchemy, and PostgreSQL.

## ✨ Features

- ✅ **Create**: Add new books to your collection
- ✅ **Read**: View all books in a clean, organized table
- ✅ **Update**: Edit existing book information
- ✅ **Delete**: Remove books from your collection (with confirmation)
- ✅ **Form Validation**: Required fields and data type validation
- ✅ **Flash Messages**: User feedback for all actions
- ✅ **Responsive Design**: Bootstrap 5 for mobile-friendly interface
- ✅ **Timestamps**: Automatic created_at and updated_at tracking
- ✅ **PostgreSQL Database**: Production-ready relational database

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask 3.0
- **ORM**: SQLAlchemy 3.1
- **Database**: PostgreSQL
- **Frontend**: Jinja2 Templates, Bootstrap 5, Bootstrap Icons
- **Architecture**: Flask Blueprints (modular design)

## 📁 Project Structure

```
book_tracker/
│
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
│
├── instance/
│   └── config.py         # Database credentials (not in git)
│
├── models/
│   └── book.py           # Book model (SQLAlchemy ORM)
│
├── routes/
│   └── book_routes.py    # All CRUD routes
│
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Homepage (list books)
│   ├── add_book.html     # Add book form
│   └── edit_book.html    # Edit book form
│
├── static/
│   ├── styles.css        # Custom CSS styles
│   └── script.js         # JavaScript enhancements
│
└── .gitignore            # Git ignore rules
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone/Download the Project

```bash
cd ~/Desktop
# The book_tracker folder should already be here
cd book_tracker
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up PostgreSQL Database

#### Install PostgreSQL (if not installed)

**macOS (using Homebrew):**
```bash
brew install postgresql@14
brew services start postgresql@14
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Create Database and User

```bash
# Connect to PostgreSQL
psql postgres

# In PostgreSQL prompt, run these commands:
CREATE DATABASE booktracker_db;
CREATE USER booktracker_user WITH PASSWORD 'booktracker_pass';
GRANT ALL PRIVILEGES ON DATABASE booktracker_db TO booktracker_user;

# PostgreSQL 15+ requires additional permission:
\c booktracker_db
GRANT ALL ON SCHEMA public TO booktracker_user;

# Exit PostgreSQL
\q
```

### Step 5: Configure Database Connection

The database configuration is already set in `instance/config.py`:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://booktracker_user:booktracker_pass@localhost:5432/booktracker_db"
```

**If you used different credentials**, update the `instance/config.py` file accordingly.

### Step 6: Run the Application

```bash
# Make sure virtual environment is activated
python app.py
```

The application will:
1. Start on `http://localhost:5000`
2. Automatically create database tables on first run
3. Be ready to use immediately

### Step 7: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### Adding a Book

1. Click "Add New Book" button on homepage
2. Fill in the form:
   - **Title** (required): Book title
   - **Author** (required): Author name
   - **Genre** (required): Book genre
   - **Year Published** (required): Publication year
   - **Description** (optional): Brief description
3. Click "Add Book"

### Viewing Books

- All books are displayed on the homepage in a table
- Shows: Title, Author, Genre, Year, Description preview
- Includes action buttons for Edit and Delete

### Editing a Book

1. Click the yellow "Edit" button next to any book
2. Modify the pre-filled form fields
3. Click "Update Book"

### Deleting a Book

1. Click the red "Delete" button next to any book
2. Confirm the deletion in the popup dialog
3. Book will be permanently removed

## 🗃️ Database Schema

### Books Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| title | String(200) | Not Null |
| author | String(100) | Not Null |
| genre | String(50) | Not Null |
| year_published | Integer | Not Null |
| description | Text | Nullable |
| created_at | DateTime | Default: now() |
| updated_at | DateTime | Default: now(), Auto-update |

## 🔒 Security Features

- POST method required for delete operations (no GET deletes)
- Form validation on both client and server side
- SQL injection protection via SQLAlchemy ORM
- CSRF protection via Flask session
- Database credentials in separate config file (not in version control)

## 🐛 Troubleshooting

### Database Connection Error

```
Error: could not connect to server
```

**Solution**: Make sure PostgreSQL is running:
```bash
# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql
```

### Module Not Found Error

```
ModuleNotFoundError: No module named 'flask'
```

**Solution**: Activate virtual environment and install dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution**: Either kill the process using port 5000 or change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Tables Not Created

**Solution**: The tables are created automatically on first run. If issues persist:
```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Tables created!')"
```

## 🧪 Testing the Application

### Manual Testing Checklist

- [ ] Add a new book successfully
- [ ] View books on homepage
- [ ] Edit an existing book
- [ ] Delete a book (with confirmation)
- [ ] Form validation works (required fields)
- [ ] Flash messages appear for all actions
- [ ] Timestamps are recorded correctly

### Sample Test Data

Add these books for testing:

1. **Title**: "The Great Gatsby", **Author**: "F. Scott Fitzgerald", **Genre**: "Fiction", **Year**: 1925
2. **Title**: "1984", **Author**: "George Orwell", **Genre**: "Science Fiction", **Year**: 1949
3. **Title**: "To Kill a Mockingbird", **Author**: "Harper Lee", **Genre**: "Fiction", **Year**: 1960

## 🚢 Deployment

For production deployment, consider:

1. **Using Gunicorn** as WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set environment variables**:
   ```bash
   export FLASK_ENV=production
   export DATABASE_URL=your_production_database_url
   ```

3. **Use proper secret key**:
   Update `SECRET_KEY` in instance/config.py with a secure random key

## 📝 Development Notes

### Adding New Features

To add new fields to the Book model:

1. Update `models/book.py`
2. Update form templates (`add_book.html`, `edit_book.html`)
3. Update table display in `index.html`
4. Update routes in `routes/book_routes.py`

### Database Migrations

For production, consider using Flask-Migrate:
```bash
pip install Flask-Migrate
```

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as a demonstration of Flask + SQLAlchemy CRUD operations with PostgreSQL.

## 🙏 Acknowledgments

- Flask Documentation
- SQLAlchemy Documentation
- Bootstrap 5
- Bootstrap Icons
