# Collaborative Project Management API

A RESTful API for managing collaborative software projects, tasks, team members, documents, comments, timeline events, and notifications.

The project is built using Django and Django REST Framework and uses JWT authentication for secure API access.

---

## 1. Project Overview

The Collaborative Project Management API provides backend functionality for managing software development projects.

The system supports:

- User registration
- User authentication
- JWT access and refresh tokens
- User logout
- User profiles
- Project management
- Team members
- Task management
- Task assignment
- Document management
- File uploads
- Comments and discussions
- Timeline events
- Notifications
- Notification read/unread status
- Role-based permissions

---

## 2. Technology Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite
- Pillow
- Git
- GitHub
- Postman

---

## 3. Project Structure

```text
Collaborative-Project-Management-API/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
│
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md