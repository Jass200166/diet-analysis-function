# Diet Analysis Project — CPSY‑300

This is my Diet Analysis project for CPSY‑300 at SAIT.  
It includes an Azure Functions backend and a simple dashboard made with HTML + JavaScript.  
Everything runs locally on my computer.

---

## Project Structure

diet-analysis-project/
│
├── diet-analysis-function/   ← backend (Azure Functions)
├── dashboard/                ← frontend (HTML pages)
└── README.md                 ← this file

---

## How to Run the Backend (Azure Functions)

1. Open PowerShell
2. Go to the backend folder:

   cd diet-analysis-function

3. Activate the virtual environment:

   .\.venv\Scripts\Activate.ps1

4. Start Azure Functions:

   func start

If it works, you will see:

http://localhost:7071/api/{*route}

---

## API Endpoints

### Login API
POST → /api/login  
Body:

{
  "email": "test@sait.ca",
  "password": "password123"
}

Expected result:

{"success": true}

### Recipes API
GET → /api/recipes?page=1

This returns recipe data from the CSV file.

---

## How to Open the Dashboard

The dashboard is just HTML files, so you open them normally.

### Option 1 — Double‑click
Open:

- login.html
- index.html

### Option 2 — VS Code Live Server
Right‑click login.html → Open with Live Server

---

## Dashboard Features

### Login Page
- Sends login request to /api/login
- Saves user email
- Redirects to dashboard

### Dashboard Page
- Loads recipes from /api/recipes
- Supports diet filter
- Search
- Pagination
- Logout

If not logged in, it redirects back to login.

---



---

## Student Info

Name: Jaspreet Kaur  
Course: CPSY‑300  
School: SAIT  
Project: Diet Analysis (Azure Functions + Dashboard)
