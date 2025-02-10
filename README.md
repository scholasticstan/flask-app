# Flask Project

## Overview

This is a Flask-based web application that includes database migrations using Alembic and Flask-Migrate. The project follows best practices for structuring a Flask app and uses a relational database.

## Features

- User authentication and management
- Database migrations with Alembic
- API endpoints for application functionality
- Environment-based configurations
- Error handling and logging

## Installation

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)
- SQLite (default) or another relational database

### Setup

1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd flask_project
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create a `.env` file and add necessary configurations (example below):
     ```ini
     FLASK_APP=run.py
     FLASK_ENV=development
     SECRET_KEY=your_secret_key
     DATABASE_URL=sqlite:///database.db
     ```

## Database Migrations

To initialize and apply database migrations:

```sh
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Running the Application

To start the Flask server:

```sh
flask run
```

## Common Issues & Fixes

1. **Constraint must have a name error:**

   - Ensure all constraints (unique, foreign keys) have explicit names in migrations.
   - If issues persist, reset migrations and database:
     ```sh
     rm -rf migrations/
     flask db init
     flask db migrate -m "Reinitialized migrations"
     flask db upgrade
     ```
   - Alternatively, manually add constraint names in migration files before running `flask db upgrade`.

2. **Database connection issues:**

   - Check `.env` settings for correct `DATABASE_URL`.
   - Ensure required database drivers are installed.
   - If using PostgreSQL, ensure the server is running and credentials are correct.

3. **Virtual environment activation issues:**
   - If `source venv/bin/activate` fails on macOS/Linux, ensure the script has execution permissions:
     ```sh
     chmod +x venv/bin/activate
     ```
   - On Windows, use `venv\Scripts\activate.bat` in Command Prompt or `venv\Scripts\Activate.ps1` in PowerShell (ensure execution policy allows running scripts).

## Contributing

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Added new feature"`)
4. Push to GitHub (`git push origin feature-name`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See `LICENSE` for details.
