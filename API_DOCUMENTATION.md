# Collaborative Project Management API

## API Documentation

A Django REST Framework based API for managing collaborative software projects, team members, tasks, documents, comments, timeline events, and user notifications.

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [API Base URL](#3-api-base-url)
4. [Authentication](#4-authentication)
5. [User Roles](#5-user-roles)
6. [Data Models](#6-data-models)
7. [HTTP Status Codes](#7-http-status-codes)
8. [Ticket 1 - User Registration](#8-ticket-1---user-registration-api)
9. [Ticket 2 - User Login](#9-ticket-2---user-login-api)
10. [Ticket 3 - User Logout](#10-ticket-3---user-logout-api)
11. [Ticket 4 - Create Project](#11-ticket-4---create-project-api)
12. [Ticket 5 - List Projects](#12-ticket-5---list-projects-api)
13. [Ticket 6 - Project Detail](#13-ticket-6---project-detail-api)
14. [Ticket 7 - Update Project](#14-ticket-7---update-project-api)
15. [Ticket 8 - Delete Project](#15-ticket-8---delete-project-api)
16. [Ticket 9 - Create Task](#16-ticket-9---create-task-api)
17. [Ticket 10 - List Tasks](#17-ticket-10---list-tasks-api)
18. [Ticket 11 - Task Detail](#18-ticket-11---task-detail-api)
19. [Ticket 12 - Update Task](#19-ticket-12---update-task-api)
20. [Ticket 13 - Delete Task](#20-ticket-13---delete-task-api)
21. [Ticket 14 - Assign Task](#21-ticket-14---assign-task-api)
22. [Ticket 15 - Upload Document](#22-ticket-15---upload-document-api)
23. [Ticket 16 - List Documents](#23-ticket-16---list-documents-api)
24. [Ticket 17 - Document Detail](#24-ticket-17---document-detail-api)
25. [Ticket 18 - Update Document](#25-ticket-18---update-document-api)
26. [Ticket 19 - Delete Document](#26-ticket-19---delete-document-api)
27. [Ticket 20 - Create Comment](#27-ticket-20---create-comment-api)
28. [Ticket 21 - List Comments](#28-ticket-21---list-comments-api)
29. [Ticket 22 - Comment Detail](#29-ticket-22---comment-detail-api)
30. [Ticket 23 - Update Comment](#30-ticket-23---update-comment-api)
31. [Ticket 24 - Delete Comment](#31-ticket-24---delete-comment-api)
32. [Ticket 25 - Timeline Events](#32-ticket-25---timeline-events-api)
33. [Ticket 26 - Notifications](#33-ticket-26---notifications-api)
34. [Ticket 27 - Mark Notification as Read](#34-ticket-27---mark-notification-as-read-api)
35. [Validation](#35-validation)
36. [Permissions](#36-permissions)
37. [File Uploads](#37-file-uploads)
38. [Error Handling](#38-error-handling)
39. [Testing](#39-testing)
40. [Manual API Testing](#40-manual-api-testing)


---

# 1. Project Overview

The Collaborative Project Management API is a backend application developed using Django and Django REST Framework.

The API provides functionality for:

- User registration
- User authentication
- JWT login
- User logout
- User profiles
- Role management
- Project management
- Team member management
- Task management
- Task assignment
- Document management
- File uploads
- Comments and discussions
- Timeline events
- Notifications
- Marking notifications as read

The API follows REST principles and uses JSON for normal requests and responses.

Multipart form-data is used for file uploads.


---

# 2. Technology Stack

The project uses the following technologies:

- Python
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- SQLite
- Pillow
- JWT Authentication
- Django ORM

Main project structure:

```text
Collaborative-Project-Management-API/
│
├── manage.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── core/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── tests.py
│   └── migrations/
│
├── media/
│
├── db.sqlite3
│
├── requirements.txt
│
├── README.md
│
└── api_documentation.md