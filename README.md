# Task Management System

A full-stack Task Management System built with Python (Flask), PostgreSQL, and Vanilla HTML/CSS/JavaScript. It features a clean architecture, simple folder structure, and well-commented code, making it perfect for beginners.

## Features

- **User Authentication:** Registration, login, and logout using session-based authentication with secure password hashing.
- **Dashboard Overview:** Quick statistics showing total, pending, completed, and overdue tasks.
- **Task Management:** Full CRUD (Create, Read, Update, Delete) operations for tasks.
- **Task Filtering & Search:** Filter tasks by status and priority, and search by title.
- **Clean UI:** Modern, responsive, card-based interface built completely without CSS frameworks like Bootstrap or Tailwind.
- **Security:** Parameterized SQL queries to prevent SQL injection and hashed passwords (Werkzeug).

## Workflows

### User Workflow

```mermaid
graph TD
    A[Visitor] -->|Registers Account| B(Login)
    A -->|Already has Account| B
    B -->|Successful Login| C{Dashboard Overview}
    C -->|View Metrics| C
    C -->|Navigate to All Tasks| D[Tasks List]
    D -->|Click Add Task| E[Create Task Form]
    E -->|Submit New Task| D
    D -->|Click Edit Task| F[Edit Task Form]
    F -->|Update Task| D
    D -->|Quick Actions| G[Mark Complete / Pending / Delete]
    G --> D
    D -->|Use Filters| H[Search & Filter Tasks]
    H --> D
```

### System Workflow

```mermaid
graph LR
    A[User Browser] -->|HTTP Request| B(Flask App Routing)
    B -->|Check Session Cookie| C{Authentication}
    C -->|Invalid Session| D[Redirect to Login]
    C -->|Valid Session| E[Route Handler]
    E -->|Parameterized SQL| F[(PostgreSQL Database)]
    F -->|Return Fetched Data| E
    E -->|Process Data & Pass to Template| G[Jinja2 Engine]
    G -->|Render HTML with Data| H[HTTP Response]
    H -->|Deliver to Browser with CSS/JS| A
```

## Folder Structure

```text
task_manager/
│
├── app.py                 # Main Flask application and routing logic
├── config.py              # Configuration settings (database credentials)
├── requirements.txt       # Python dependencies (Flask, psycopg2-binary)
│
├── database/
│   └── schema.sql         # SQL script to create the necessary tables
│
├── static/
│   ├── css/
│   │   └── style.css      # Vanilla CSS styling
│   └── js/
│       └── main.js        # Vanilla JS for frontend interactions
│
├── templates/
│   ├── base.html          # Base Jinja2 template with navbar and layout
│   ├── login.html         # User login page
│   ├── register.html      # User registration page
│   ├── dashboard.html     # Dashboard metrics page
│   ├── tasks.html         # Tasks list, filter, and search
│   ├── add_task.html      # Form to create a new task
│   └── edit_task.html     # Form to edit an existing task
│
└── README.md              # Project documentation
```

## Installation & Setup

Follow these steps to get the project running locally.

### 1. Prerequisites

- Python 3.x
- PostgreSQL Server (or a cloud DB like Supabase)

### 2. Clone the Repository

```bash
git clone <repository-url>
cd "Task Management System"
```

### 3. PostgreSQL Setup & Database Import

1. Start your local PostgreSQL server or create a cloud database (like Supabase or Render PostgreSQL).
2. Open your PostgreSQL client (psql, pgAdmin, or DBeaver).
3. Run the SQL commands located in the `database/schema.sql` file to create the `users` and `tasks` tables.

From the command line (if local), you can do:
```bash
psql -U postgres -d task_manager -f database/schema.sql
```

### 4. Configuration

The application is configured using a single `DATABASE_URL` connection string.
Open `config.py` or set an environment variable with your PostgreSQL credentials:

```python
class Config:
    SECRET_KEY = 'your-secret-key' # Change this in production
    DATABASE_URL = 'postgresql://postgres:password@localhost:5432/task_manager'
```

### 5. Deployment (Render & Supabase)
This app is ready to deploy!
1. **Database:** Create a project on Supabase, run the `schema.sql`, and copy the Connection String URI.
2. **Web Server:** Create a Web Service on Render, connect your GitHub repo, set Build Command to `pip install -r requirements.txt` and Start Command to `gunicorn app:app`.
3. **Environment Variables:** Add `DATABASE_URL` on Render and paste the Supabase string.

### 5. Install Python Dependencies

Create a virtual environment (optional but recommended) and install the required packages:

```bash
# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Run the Flask Application

Start the development server:

```bash
python app.py
```

The application will run at `http://127.0.0.1:5000/`. Open this URL in your web browser.

---

## Screenshots


- **Login / Register**
  ![Login Screen](Screenshorts/Screenshot%202026-07-09%20215733.png)
  ![Register Screen](Screenshorts/Screenshot%202026-07-09%20215743.png)
- **Dashboard**
  ![Dashboard Screen](Screenshorts/Screenshot%202026-07-09%20215811.png)
- **Task List**
  ![Task List Screen](Screenshorts/Screenshot%202026-07-09%20215821.png)
- **Add Task**
  ![Add Task Screen](Screenshorts/Screenshot%202026-07-09%20215831.png)
  
---

## Future Improvements

- Implement pagination for the tasks list.
- Add user profile management (avatar, update password).
- Implement email notifications for overdue tasks.
- Allow grouping tasks into categories or projects.
- Add drag-and-drop ordering for tasks.

## 📄 License

This project is intended for educational and learning purposes.

---

## 👩‍💻 Author

**Aarushi Chaddha**

---

## 🏢 Internship

**These projects were developed as part of the MPOnline Internship Project.**

