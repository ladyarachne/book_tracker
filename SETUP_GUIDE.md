# 📘 Complete Setup Guide - Book Tracker Application

This comprehensive guide will walk you through setting up and running the Book Tracker application from scratch. Perfect for students and beginners!

## 📑 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installing Prerequisites](#installing-prerequisites)
3. [Setting Up PostgreSQL](#setting-up-postgresql)
4. [Project Setup](#project-setup)
5. [Running the Application](#running-the-application)
6. [Testing CRUD Operations](#testing-crud-operations)
7. [Common Issues and Solutions](#common-issues-and-solutions)

---

## 1. System Requirements

### Minimum Requirements

- **Operating System**: macOS, Linux, or Windows
- **Python**: Version 3.8 or higher
- **PostgreSQL**: Version 12 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB free space

### Check Your Python Version

Open Terminal (macOS/Linux) or Command Prompt (Windows):

```bash
python3 --version
```

Expected output: `Python 3.8.x` or higher

---

## 2. Installing Prerequisites

### macOS

#### Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Python 3

```bash
brew install python3
```

#### Install PostgreSQL

```bash
brew install postgresql@14
brew services start postgresql@14
```

### Ubuntu/Debian Linux

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Windows

1. **Install Python**:
   - Download from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation
   - Verify: `python --version`

2. **Install PostgreSQL**:
   - Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Run installer and remember the password you set for postgres user
   - Add PostgreSQL bin directory to PATH

---

## 3. Setting Up PostgreSQL

### Step 3.1: Start PostgreSQL

**macOS (Homebrew):**
```bash
brew services start postgresql@14
```

**Linux:**
```bash
sudo systemctl start postgresql
```

**Windows:**
PostgreSQL should start automatically after installation.

### Step 3.2: Access PostgreSQL

**macOS/Linux:**
```bash
psql postgres
```

**Windows:**
```bash
psql -U postgres
```

### Step 3.3: Create Database and User

Once in the PostgreSQL prompt (`postgres=#`), run these commands:

```sql
-- Create the database
CREATE DATABASE booktracker_db;

-- Create the user
CREATE USER booktracker_user WITH PASSWORD 'booktracker_pass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE booktracker_db TO booktracker_user;

-- Connect to the new database
\c booktracker_db

-- Grant schema permissions (PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO booktracker_user;

-- List databases to verify
\l

-- Exit PostgreSQL
\q
```

### Step 3.4: Verify Database Creation

```bash
psql -U booktracker_user -d booktracker_db
```

If prompted for password, enter: `booktracker_pass`

If you connect successfully, type `\q` to exit.

---

## 4. Project Setup

### Step 4.1: Navigate to Project Directory

```bash
cd ~/Desktop/book_tracker
```

### Step 4.2: Create Python Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 4.3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Expected packages to install:
- Flask==3.0.0
- Flask-SQLAlchemy==3.1.1
- psycopg2-binary==2.9.9
- python-dotenv==1.0.0

### Step 4.4: Verify Installation

```bash
pip list
```

You should see all four packages listed.

### Step 4.5: Verify Configuration

Check that `instance/config.py` has correct database credentials:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://booktracker_user:booktracker_pass@localhost:5432/booktracker_db"
```

---

## 5. Running the Application

### Step 5.1: Start the Flask Server

Make sure your virtual environment is activated (you should see `(venv)` in terminal).

```bash
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
```

### Step 5.2: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

You should see the Book Tracker homepage!

---

## 6. Testing CRUD Operations

### Test 1: CREATE - Add a Book

1. Click "Add New Book" button
2. Fill in the form:
   - **Title**: "The Great Gatsby"
   - **Author**: "F. Scott Fitzgerald"
   - **Genre**: "Fiction"
   - **Year**: 1925
   - **Description**: "A classic American novel set in the Jazz Age"
3. Click "Add Book"
4. You should see a success message and be redirected to homepage

### Test 2: READ - View Books

1. On the homepage, you should see the book you just added in the table
2. Verify all information is displayed correctly

### Test 3: UPDATE - Edit a Book

1. Click the yellow "Edit" button (pencil icon) next to your book
2. Change the description to something different
3. Click "Update Book"
4. Verify the changes are saved

### Test 4: DELETE - Remove a Book

1. Click the red "Delete" button (trash icon) next to your book
2. Confirm the deletion in the popup dialog
3. Verify the book is removed from the list

---

## 7. Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Problem**: Virtual environment not activated or packages not installed.

**Solution**:
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

### Issue 2: "could not connect to server"

**Problem**: PostgreSQL is not running.

**Solution**:
```bash
# macOS
brew services start postgresql@14

# Linux
sudo systemctl start postgresql

# Windows - Start from Services or pgAdmin
```

---

### Issue 3: "FATAL: password authentication failed"

**Problem**: Wrong database credentials.

**Solution**:
1. Verify credentials in `instance/config.py`
2. Or reset the password:
```sql
psql postgres
ALTER USER booktracker_user WITH PASSWORD 'booktracker_pass';
\q
```

---

### Issue 4: "Port 5000 already in use"

**Problem**: Another application is using port 5000.

**Solution 1 - Change Port**:
Edit `app.py`, line 47:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Solution 2 - Kill Process (macOS/Linux)**:
```bash
lsof -ti:5000 | xargs kill -9
```

---

### Issue 5: Database tables not created

**Problem**: Tables weren't created automatically.

**Solution**:
```bash
python3 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Tables created successfully!')"
```

---

### Issue 6: "relation 'books' does not exist"

**Problem**: Database tables not created.

**Solution**: Same as Issue 5 above.

---

## 8. Verifying Database Tables

You can verify tables were created correctly:

```bash
psql -U booktracker_user -d booktracker_db
```

In PostgreSQL prompt:
```sql
-- List all tables
\dt

-- Describe books table structure
\d books

-- View all books
SELECT * FROM books;

-- Exit
\q
```

---

## 9. Stopping the Application

To stop the Flask server:
- Press `CTRL+C` in the terminal

To deactivate the virtual environment:
```bash
deactivate
```

---

## 10. Restarting the Application

**Every time you want to run the app:**

1. Open Terminal and navigate to project:
   ```bash
   cd ~/Desktop/book_tracker
   ```

2. Activate virtual environment:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open browser to `http://localhost:5000`

---

## 11. Next Steps

### Add More Features

- Search functionality
- Filtering by genre
- User authentication
- Book cover images
- Reading status (Read, Currently Reading, Want to Read)

### Learn More

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/)

---

## 12. Getting Help

If you encounter issues not covered in this guide:

1. Check the error message carefully
2. Search for the error on Google or Stack Overflow
3. Review the Flask and SQLAlchemy documentation
4. Check PostgreSQL logs for database-related issues

---

## Summary Checklist

Before running the application, ensure:

- [ ] Python 3.8+ is installed
- [ ] PostgreSQL is installed and running
- [ ] Database `booktracker_db` is created
- [ ] User `booktracker_user` exists with correct permissions
- [ ] Virtual environment is created and activated
- [ ] All Python packages are installed
- [ ] Configuration file has correct database credentials
- [ ] Application runs without errors
- [ ] Can access application in browser
- [ ] All CRUD operations work correctly

---

**Congratulations!** 🎉 You've successfully set up and tested the Book Tracker application!
