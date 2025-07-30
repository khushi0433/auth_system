# User Authentication System

A simple and secure user authentication system built with Python Flask and MySQL.

## Features

- ✅ User Registration with validation
- ✅ Secure password hashing (bcrypt)
- ✅ User Login with session management
- ✅ Protected dashboard area
- ✅ Remember Me functionality
- ✅ Secure logout
- ✅ Input validation and error handling
- ✅ Responsive design
- ✅ Flash messaging system

## Tech Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Password Hashing**: bcrypt
- **Frontend**: HTML5, CSS3
- **Session Management**: Flask Sessions

## Prerequisites

Before running this application, make sure you have:

- Python 3.7+ installed
- MySQL Server installed and running
- pip (Python package installer)

## Installation & Setup

### 1. Clone or Download the Project

\`\`\`bash
# If using git
git clone <repository-url>
cd flask-auth-system

# Or download and extract the ZIP file
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Database Setup

1. **Start MySQL Server** (make sure MySQL is running)

2. **Create Database and Table**:
   \`\`\`bash
   # Login to MySQL
   mysql -u root -p
   
   # Run the database setup script
   source database_setup.sql
   
   # Or copy and paste the SQL commands from database_setup.sql
   \`\`\`

3. **Update Database Configuration**:
   - Copy \`.env.example\` to \`.env\`
   - Update the database credentials in \`.env\` file:
   \`\`\`
   DB_PASSWORD=your_actual_mysql_password
   \`\`\`

### 5. Run the Application

\`\`\`bash
python app.py
\`\`\`

The application will start on \`http://localhost:5000\`

## Usage

### 1. Register a New Account
- Navigate to \`http://localhost:5000\`
- Click "Register here" or go to \`/register\`
- Fill in your details:
  - Full Name
  - Email (must be valid format)
  - Password (minimum 6 characters with letters and numbers)
  - Confirm Password
- Click "Register"

### 2. Login
- Go to \`/login\` or click "Login here"
- Enter your email and password
- Optionally check "Remember Me" for persistent sessions
- Click "Login"

### 3. Dashboard
- After successful login, you'll be redirected to the dashboard
- View your user information
- Access protected content

### 4. Logout
- Click the "Logout" button on the dashboard
- You'll be redirected to the login page

## Project Structure

\`\`\`
flask-auth-system/
│
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── database_setup.sql    # Database schema
├── .env.example         # Environment variables template
├── README.md            # This file
│
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── register.html    # Registration page
    ├── login.html       # Login page
    └── dashboard.html   # Dashboard page
\`\`\`

## Security Features

- **Password Hashing**: Uses bcrypt for secure password storage
- **Session Management**: Secure session handling with Flask
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: Uses parameterized queries
- **CSRF Protection**: Can be easily added with Flask-WTF
- **Environment Variables**: Sensitive data stored in environment variables

## Database Schema

\`\`\`sql
users table:
- id (INT, PRIMARY KEY, AUTO_INCREMENT)
- full_name (VARCHAR(100), NOT NULL)
- email (VARCHAR(100), UNIQUE, NOT NULL)
- password (VARCHAR(255), NOT NULL) # Hashed with bcrypt
- created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
- updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE)
\`\`\`

## Validation Rules

### Registration:
- Full Name: Required, non-empty
- Email: Required, valid email format, unique
- Password: Minimum 6 characters, must contain letters and numbers
- Confirm Password: Must match password

### Login:
- Email: Required, valid format
- Password: Required

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid input data
- Duplicate email registration
- Incorrect login credentials
- Session management errors

## Troubleshooting

### Common Issues:

1. **Database Connection Error**:
   - Ensure MySQL server is running
   - Check database credentials in \`.env\` file
   - Verify database and table exist

2. **Module Import Errors**:
   - Make sure virtual environment is activated
   - Install all requirements: \`pip install -r requirements.txt\`

3. **Permission Errors**:
   - Check MySQL user permissions
   - Ensure database user can create/read/write

4. **Port Already in Use**:
   - Change port in app.py: \`app.run(debug=True, port=5001)\`

## Future Enhancements

- Email verification for new accounts
- Password reset functionality
- User profile management
- Role-based access control
- Two-factor authentication
- Rate limiting for login attempts

## License

This project is created for educational purposes as part of an internship task.
\`\`\`
