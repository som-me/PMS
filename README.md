# 🧩 Project Management System (PMS)

![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-13+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0+-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

---

## 🚀 Overview

**Project Management System (PMS)** is a full-stack web application designed for teams to efficiently **create, manage, and track projects and tasks** with clear role-based access.

This project uses:
- 🧠 **FastAPI** for backend (Python)
- ⚛️ **Next.js 13** for frontend (React)
- 🎨 **Tailwind CSS** for styling

You can **log in**, **create projects**, **add tasks**, and **manage workflows** — all through a modern dashboard interface.

---

## 🌟 Key Features

### 👥 Authentication & Roles
- Secure JWT-based login and registration  
- Role-based permissions: `Admin`, `Manager`, and `Developer`  
- Custom access control for sensitive operations  

### 📁 Project Management
- Create, edit, and view projects  
- Display project description and status  
- Assign multiple tasks to each project  

### ✅ Task Management
- Add tasks directly within project cards  
- Edit or update existing tasks inline  
- View all tasks for each project instantly  
- Role restrictions (Admin/Manager editable only)  

### 💻 Dashboard
- Interactive project cards  
- “Add Task” → opens a modal  
- Once a task is added → converts to “Edit Task” button  
- Real-time task listing below the project card  
- Fully responsive layout  

---

## 🧩 Tech Stack

### 🔹 Frontend
- Next.js 13  
- React  
- Tailwind CSS  
- Recharts (for visualization)
- Fetch API with JWT authorization headers  

### 🔹 Backend
- FastAPI  
- SQLAlchemy ORM  
- JWT (OAuth2PasswordBearer)  
- SQLite (easily switchable to PostgreSQL/MySQL)  
- Pydantic schemas  

---

## 🗂️ Project Structure

PMS/
│
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI entry point
│ │ ├── models.py # SQLAlchemy models (User, Project, Task)
│ │ ├── schemas.py # Pydantic schemas
│ │ ├── deps.py # Auth & DB dependencies
│ │ ├── auth.py # Auth routes (register, login)
│ │ ├── projects.py # Project CRUD routes
│ │ ├── tasks.py # Task CRUD routes (Create, Edit, Get by Project)
│ │ └── database.py # DB engine setup
│ └── requirements.txt
│
├── frontend/
│ ├── components/
│ │ ├── ProjectCard.js
│ │ ├── CreateProjectModal.js
│ │ ├── TaskCard.js
│ │ └── CreateTaskModal.js
│ ├── app/
│ │ ├── page.js # Auth page (Login/Register)
│ │ └── dashboard/page.js # Dashboard page
│ └── package.json
│
└── README.md


---

## ⚙️ Setup Guide

### 🧱 1️⃣ Clone the Repository

```bash
git clone https://github.com/som-me/PMS.git
cd PMS


⚙️ 2️⃣ Backend Setup (FastAPI)
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# or
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
uvicorn app.main:app --reload

Your backend will be live at:
👉 http://127.0.0.1:8000

You can test the API at:
Swagger UI: http://127.0.0.1:8000/docs

Test endpoint: /api/auth/test

💻 3️⃣ Frontend Setup (Next.js)

cd ../frontend
npm install
npm run dev

Your frontend will be live at:
👉 http://localhost:3000

🌍 Frontend

Inside:

frontend/components/AuthForm.js

frontend/app/dashboard/page.js

Update:

const BACKEND_URL = "http://127.0.0.1:8000";

