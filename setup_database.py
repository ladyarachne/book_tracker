#!/usr/bin/env python3
"""
Database Setup Script for Book Tracker Application
This script creates the PostgreSQL database, user, and tables automatically.
"""

import sys
import subprocess
from getpass import getpass

def run_command(command, description):
    """Execute a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {description} failed!")
        if e.stderr:
            print(f"Error message: {e.stderr}")
        return False

def check_postgresql_installed():
    """Check if PostgreSQL is installed and running."""
    print("\n" + "="*60)
    print("Checking PostgreSQL Installation")
    print("="*60)
    
    # Check if psql command exists
    result = subprocess.run(
        "which psql",
        shell=True,
        capture_output=True
    )
    
    if result.returncode != 0:
        print("✗ PostgreSQL is not installed or not in PATH!")
        print("\nPlease install PostgreSQL first:")
        print("  macOS: brew install postgresql@14")
        print("  Ubuntu: sudo apt install postgresql postgresql-contrib")
        print("  Windows: Download from https://www.postgresql.org/download/windows/")
        return False
    
    print("✓ PostgreSQL is installed!")
    return True

def create_database():
    """Create the database and user in PostgreSQL."""
    print("\n" + "="*60)
    print("Setting Up Database")
    print("="*60)
    
    print("\nThis script will create:")
    print("  - Database: booktracker_db")
    print("  - User: booktracker_user")
    print("  - Password: booktracker_pass")
    
    # Ask for PostgreSQL admin password
    print("\nYou may be prompted for your PostgreSQL admin password.")
    
    # Create SQL commands
    sql_commands = """
    -- Create database if it doesn't exist
    SELECT 'CREATE DATABASE booktracker_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'booktracker_db')\\gexec
    
    -- Create user if it doesn't exist
    DO
    $$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'booktracker_user') THEN
            CREATE USER booktracker_user WITH PASSWORD 'booktracker_pass';
        END IF;
    END
    $$;
    
    -- Grant privileges
    GRANT ALL PRIVILEGES ON DATABASE booktracker_db TO booktracker_user;
    
    -- Connect to booktracker_db and grant schema permissions
    \\c booktracker_db
    GRANT ALL ON SCHEMA public TO booktracker_user;
    """
    
    # Write SQL to temporary file
    with open('/tmp/setup_booktracker.sql', 'w') as f:
        f.write(sql_commands)
    
    # Execute SQL commands
    success = run_command(
        "psql postgres -f /tmp/setup_booktracker.sql",
        "Creating database and user"
    )
    
    # Clean up
    subprocess.run("rm /tmp/setup_booktracker.sql", shell=True)
    
    return success

def create_tables():
    """Create application tables using Flask."""
    print("\n" + "="*60)
    print("Creating Database Tables")
    print("="*60)
    
    try:
        from app import app, db
        
        with app.app_context():
            db.create_all()
            print("✓ Database tables created successfully!")
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'books' in tables:
                print("\nCreated tables:")
                for table in tables:
                    print(f"  - {table}")
                return True
            else:
                print("✗ Error: Books table was not created!")
                return False
                
    except Exception as e:
        print(f"✗ Error creating tables: {str(e)}")
        return False

def verify_setup():
    """Verify the database setup."""
    print("\n" + "="*60)
    print("Verifying Setup")
    print("="*60)
    
    # Test database connection
    test_command = "psql -U booktracker_user -d booktracker_db -c '\\dt' -c '\\q'"
    
    print("\nTesting database connection...")
    result = subprocess.run(
        test_command,
        shell=True,
        capture_output=True,
        text=True,
        env={'PGPASSWORD': 'booktracker_pass'}
    )
    
    if result.returncode == 0:
        print("✓ Database connection successful!")
        print("\nDatabase tables:")
        print(result.stdout)
        return True
    else:
        print("✗ Database connection failed!")
        print(result.stderr)
        return False

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("Book Tracker - Database Setup Script")
    print("="*60)
    
    # Check prerequisites
    if not check_postgresql_installed():
        sys.exit(1)
    
    # Create database and user
    if not create_database():
        print("\n✗ Database setup failed! Please check the errors above.")
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        print("\n✗ Table creation failed! Please check the errors above.")
        sys.exit(1)
    
    # Verify setup
    if verify_setup():
        print("\n" + "="*60)
        print("✓ Setup Complete!")
        print("="*60)
        print("\nYour Book Tracker application is ready!")
        print("\nTo start the application:")
        print("  1. Activate virtual environment: source venv/bin/activate")
        print("  2. Run the app: python app.py")
        print("  3. Open browser to: http://localhost:5000")
        print("\nDatabase credentials:")
        print("  Database: booktracker_db")
        print("  User: booktracker_user")
        print("  Password: booktracker_pass")
        print("  Host: localhost")
        print("  Port: 5432")
    else:
        print("\n✗ Setup verification failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
