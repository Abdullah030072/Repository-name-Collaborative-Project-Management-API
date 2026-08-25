# Collaborative Project Management API
# Complete API Documentation

**Project:** Collaborative Project Management API  
**Framework:** Django + Django REST Framework  
**Authentication:** JWT (JSON Web Token)  
**Database:** SQLite  
**API Base URL:** `http://127.0.0.1:8000/api/`

---

# Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Authentication](#3-authentication)
4. [User and Profile APIs](#4-user-and-profile-apis)
5. [Project Management APIs](#5-project-management-apis)
6. [Task Management APIs](#6-task-management-apis)
7. [Document Management APIs](#7-document-management-apis)
8. [Comment and Discussion APIs](#8-comment-and-discussion-apis)
9. [Timeline Events API](#9-timeline-events-api)
10. [Notifications APIs](#10-notifications-apis)
11. [HTTP Status Codes](#11-http-status-codes)
12. [Permissions](#12-permissions)
13. [Validation](#13-validation)
14. [File Upload](#14-file-upload)
15. [JWT Authentication Flow](#15-jwt-authentication-flow)
16. [API Testing](#16-api-testing)
17. [Complete API Endpoint List](#17-complete-api-endpoint-list)
18. [Project Working Flow](#18-project-working-flow)

---

# 1. Project Overview

The Collaborative Project Management API is a RESTful backend application developed using Django and Django REST Framework.

The purpose of this application is to provide a centralized platform for managing collaborative software projects.

The system allows authenticated users to:

- Register accounts
- Login using JWT authentication
- Logout and invalidate refresh tokens
- Create and manage projects
- Add project team members
- Create and manage tasks
- Assign tasks to team members
- Upload project documents
- Manage document versions
- Create comments
- Update and delete personal comments
- View project timeline events
- Receive notifications
- Mark notifications as read

The API follows REST principles and uses HTTP methods such as:

- GET
- POST
- PUT
- PATCH
- DELETE

---

# 2. Technology Stack

The project uses the following technologies:

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend web framework |
| Django REST Framework | REST API development |
| Simple JWT | JWT authentication |
| SQLite | Development database |
| Pillow | ImageField support |
| Git | Version control |
| GitHub | Source code repository |
| Postman | Manual API testing |

---

# 3. Authentication

The application uses JWT authentication.

JWT stands for:

**JSON Web Token**

After successfully logging in, the API returns:

```json
{
    "refresh": "refresh-token",
    "access": "access-token"
}

The access token is used when accessing protected APIs.

For authenticated requests, send the access token in the request header:

Authorization: Bearer <access-token>

Example:

Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Ticket 1 - User Registration API
Endpoint
POST /api/register/
Purpose

This API allows a new user to create an account.

The endpoint is publicly accessible, so authentication is not required.

Authentication Required

No.

AllowAny
Request Body

Content-Type:

application/json

Example:

{
    "username": "abdullah",
    "email": "abdullah@example.com",
    "password": "StrongPassword123"
}
Required Fields
Field	Required	Description
username	Yes	Unique username
email	Yes	User email
password	Yes	Account password
Example Request
POST /api/register/
Content-Type: application/json
{
    "username": "abdullah",
    "email": "abdullah@example.com",
    "password": "StrongPassword123"
}
Successful Response

Status:

201 Created

Example:

{
    "id": 1,
    "username": "abdullah",
    "email": "abdullah@example.com"
}
Possible Errors
Duplicate username
400 Bad Request

Example:

{
    "username": [
        "A user with that username already exists."
    ]
}
Duplicate email
400 Bad Request
Missing password
400 Bad Request
Working

The registration request is passed to UserSerializer.

The serializer removes the password from the validated data and uses Django's:

User.objects.create_user()

This ensures the password is hashed instead of being stored as plain text.

Ticket 2 - User Login API
Endpoint
POST /api/login/
Purpose

Allows a registered user to authenticate and receive JWT access and refresh tokens.

Authentication Required

No.

Request Body
{
    "username": "abdullah",
    "password": "StrongPassword123"
}
Required Fields
Field	Required
username	Yes
password	Yes
Successful Response

Status:

200 OK

Example:

{
    "refresh": "refresh-token",
    "access": "access-token"
}
Invalid Credentials

Status:

401 Unauthorized

Example:

{
    "detail": "No active account found with the given credentials"
}
Working

The API uses:

TokenObtainPairView

from Simple JWT.

The user provides valid credentials.

The system verifies the username and password.

If authentication succeeds:

Access token is generated.
Refresh token is generated.
Both tokens are returned to the client.

The access token is used for API requests.

The refresh token is used to obtain a new access token after the access token expires.

Ticket 3 - User Logout API
Endpoint
POST /api/logout/
Purpose

Logs the authenticated user out.

The refresh token is blacklisted so it can no longer be used.

Authentication Required

Yes.

IsAuthenticated
Request Body
{
    "refresh": "refresh-token"
}
Required Fields
Field	Required
refresh	Yes
Successful Response

Status:

205 Reset Content

Example:

{
    "detail": "Successfully logged out."
}
Missing Refresh Token

Status:

400 Bad Request

Example:

{
    "detail": "Refresh token is required."
}
Invalid Refresh Token

Status:

400 Bad Request

Example:

{
    "detail": "Invalid or expired refresh token."
}
Working

The API receives the refresh token.

It creates a RefreshToken object and calls:

token.blacklist()

The refresh token is then added to the blacklist.

User APIs
User List API

Although not part of the numbered ticket list, the project also contains a user listing API.

Endpoint
GET /api/users/
Authentication

Currently:

AllowAny
Successful Response
200 OK

Example:

[
    {
        "id": 1,
        "username": "abdullah",
        "email": "abdullah@example.com"
    }
]
Profile APIs

The project contains profile APIs for managing:

Profile picture
Role
Contact number
User relationship

Available roles include:

manager
qa
developer
Profile List/Create API
Endpoint
GET /api/profiles/
POST /api/profiles/
Authentication

Currently:

AllowAny
Example POST
{
    "profile_picture": null,
    "role": "developer",
    "contact_number": "03001234567"
}

The user field is read-only.

Profile Detail API
Endpoint
GET /api/profiles/{profile_id}/
PUT /api/profiles/{profile_id}/
PATCH /api/profiles/{profile_id}/

Example:

GET /api/profiles/1/
5. Project Management APIs

Projects are the main containers for tasks, documents, comments, timeline events and team members.

The Project model contains:

title
description
start_date
end_date
created_by
team_members
created_at
updated_at
Ticket 4 - Create Project API
Endpoint
POST /api/projects/
Purpose

Creates a new project.

Authentication Required

Yes.

Required Permission

Manager.

The manager role is checked using:

IsManager
Request Body
{
    "title": "Website Development",
    "description": "Development of company website",
    "start_date": "2026-08-25",
    "end_date": "2026-09-25",
    "team_members": [2, 3]
}
Required Fields
Field	Required
title	Yes
description	No
start_date	No
end_date	No
team_members	No
Successful Response
201 Created

Example:

{
    "id": 1,
    "title": "Website Development",
    "description": "Development of company website",
    "start_date": "2026-08-25",
    "end_date": "2026-09-25",
    "created_by": {
        "id": 1,
        "username": "manager",
        "email": "manager@example.com"
    },
    "team_members": [2, 3],
    "created_at": "...",
    "updated_at": "..."
}
Permission Error

A non-manager cannot create a project.

Expected status:

403 Forbidden
Ticket 5 - List Projects API
Endpoint
GET /api/projects/
Purpose

Returns projects visible through the API.

Authentication Required

Yes.

IsAuthenticated
Example Request
GET /api/projects/
Authorization: Bearer <access-token>
Successful Response
200 OK

Example:

[
    {
        "id": 1,
        "title": "Website Development",
        "description": "Company website",
        "start_date": "2026-08-25",
        "end_date": "2026-09-25"
    }
]
Ticket 6 - Project Detail API
Endpoint
GET /api/projects/{project_id}/

Example:

GET /api/projects/1/
Authentication

Yes.

Successful Response
200 OK

Returns detailed information about the project.

Project Not Found
404 Not Found
Ticket 7 - Update Project API
Endpoint
PUT /api/projects/{project_id}/

Partial updates are also supported through:

PATCH /api/projects/{project_id}/
Authentication

Yes.

Permission

Manager.

Example
{
    "title": "Updated Website Project",
    "description": "Updated description",
    "start_date": "2026-08-26",
    "end_date": "2026-10-01",
    "team_members": [2, 3]
}
Success
200 OK
Ticket 8 - Delete Project API
Endpoint
DELETE /api/projects/{project_id}/
Authentication

Yes.

Permission

Manager.

Success
204 No Content
Working

The selected project is deleted from the database.

Because related models use appropriate foreign-key relationships, related records can also be affected according to their configured on_delete behavior.

6. Task Management APIs

Tasks belong to projects.

A task contains:

title
description
status
project
assignee
created_at
updated_at

Available statuses:

open
review
working
awaiting_release
waiting_qa
Ticket 9 - Create Task API
Endpoint
POST /api/tasks/
Authentication

Yes.

Permission

Manager.

Example Request
{
    "title": "Create Login Page",
    "description": "Develop login page",
    "status": "open",
    "project": 1,
    "assignee": 2
}
Required Fields
Field	Required
title	Yes
description	No
status	No
project	Yes
assignee	No
Success
201 Created
Ticket 10 - List Tasks API
Endpoint
GET /api/tasks/
Authentication

Yes.

Permission

Authenticated user.

Success
200 OK

Example:

[
    {
        "id": 1,
        "title": "Create Login Page",
        "description": "Develop login page",
        "status": "open",
        "project": 1,
        "assignee": 2
    }
]
Ticket 11 - Task Detail API
Endpoint
GET /api/tasks/{task_id}/

Example:

GET /api/tasks/1/
Authentication

Yes.

Success
200 OK
Ticket 12 - Update Task API
Endpoint
PUT /api/tasks/{task_id}/

or:

PATCH /api/tasks/{task_id}/
Authentication

Yes.

Permission

Manager.

Example
{
    "title": "Updated Login Task",
    "description": "Updated task description",
    "status": "working",
    "project": 1,
    "assignee": 2
}
Success
200 OK
Ticket 13 - Delete Task API
Endpoint
DELETE /api/tasks/{task_id}/
Authentication

Yes.

Permission

Manager.

Success
204 No Content
Ticket 14 - Assign Task API
Endpoint
POST /api/tasks/{task_id}/assign/
Purpose

Assigns a task to a project team member.

Authentication

Yes.

Permission

Manager.

Request Body
{
    "assignee": 2
}
Required Field
assignee
Successful Response
200 OK

Example:

{
    "id": 1,
    "title": "Login Task",
    "description": "Create login page",
    "status": "open",
    "project": 1,
    "assignee": 2
}
Missing Assignee
400 Bad Request
{
    "detail": "Assignee is required."
}
User Not Found
404 Not Found
{
    "detail": "User not found."
}
User Not In Project
400 Bad Request
{
    "detail": "User is not a member of this project."
}
Working

The API:

Finds the task.
Gets the assignee ID.
Finds the user.
Checks whether the user belongs to the task's project.
Assigns the user.
Saves the task.
Returns the updated task.
7. Document Management APIs

Documents are associated with projects.

The Document model contains:

name
description
file
version
project
created_at
updated_at

Documents are uploaded using multipart form data.

Ticket 15 - Upload Document API
Endpoint
POST /api/documents/
Authentication

Yes.

Content Type
multipart/form-data
Example Form Data
name = Project Requirements
description = Initial requirements document
version = 1.0
project = 1
file = requirements.pdf
Required Fields
Field	Required
name	Yes
description	No
file	Yes
version	No
project	Yes
Success
201 Created
Ticket 16 - List Documents API
Endpoint
GET /api/documents/list/
Authentication

Yes.

Success
200 OK

Example:

[
    {
        "id": 1,
        "name": "Requirements",
        "description": "Project requirements",
        "file": "/media/documents/requirements.pdf",
        "version": "1.0",
        "project": 1
    }
]
Ticket 17 - Document Detail API
Endpoint
GET /api/documents/{document_id}/

Example:

GET /api/documents/1/
Authentication

Yes.

Success
200 OK
Not Found
404 Not Found
Ticket 18 - Update Document API
Endpoint
PUT /api/documents/{document_id}/

or:

PATCH /api/documents/{document_id}/
Authentication

Yes.

Content Type

For file-related updates:

multipart/form-data

Example:

name = Updated Requirements
description = Updated requirements
version = 2.0
project = 1

A new file can also be supplied if required.

Success
200 OK
Ticket 19 - Delete Document API
Endpoint
DELETE /api/documents/{document_id}/
Authentication

Yes.

Success
204 No Content
8. Comment and Discussion APIs

Comments allow users to participate in discussions related to:

Tasks
Projects

The Comment model contains:

text
author
created_at
task
project

The author is automatically assigned from the authenticated user.

Ticket 20 - Create Comment API
Endpoint
POST /api/comments/
Authentication

Yes.

Request Body
{
    "text": "The login page is ready for review.",
    "task": 1,
    "project": 1
}
Required Fields
Field	Required
text	Yes
task	No
project	No
Important

The author field is not provided by the client.

The API automatically uses:

self.request.user
Success
201 Created

Example:

{
    "id": 1,
    "text": "The login page is ready for review.",
    "author": 2,
    "created_at": "...",
    "task": 1,
    "project": 1
}
Ticket 21 - List Comments API
Endpoint
GET /api/comments/list/
Authentication

Yes.

Success
200 OK

Returns comments available through the endpoint.

Ticket 22 - Comment Detail API
Endpoint
GET /api/comments/{comment_id}/

Example:

GET /api/comments/1/
Authentication

Yes.

Success
200 OK
Ticket 23 - Update Comment API
Endpoint
PUT /api/comments/{comment_id}/

or:

PATCH /api/comments/{comment_id}/
Authentication

Yes.

Permission

Users can update their own comments.

Example
{
    "text": "Updated comment",
    "task": 1,
    "project": 1
}
Success
200 OK
Other User's Comment

If a user tries to modify another user's comment:

404 Not Found

This is because the detail view restricts its queryset to:

Comment.objects.filter(
    author=self.request.user
)
Ticket 24 - Delete Comment API
Endpoint
DELETE /api/comments/{comment_id}/
Authentication

Yes.

Permission

Users can delete their own comments.

Success
204 No Content
Other User's Comment

Returns:

404 Not Found

This prevents users from deleting comments belonging to other users.

9. Timeline Events API

Timeline events represent project activity.

The TimelineEvent model contains:

project
event_type
description
created_by
created_at
Ticket 25 - List Timeline Events API
Endpoint
GET /api/timeline/
Authentication

Yes.

Purpose

Retrieves timeline events.

The events are sorted by newest first.

The API uses:

.order_by("-created_at")

Therefore, the most recent event appears first.

Success
200 OK

Example:

[
    {
        "id": 5,
        "project": 1,
        "event_type": "Task Updated",
        "description": "Login task moved to review.",
        "created_by": 2,
        "created_at": "2026-08-25T10:30:00Z"
    },
    {
        "id": 4,
        "project": 1,
        "event_type": "Task Created",
        "description": "New login task created.",
        "created_by": 1,
        "created_at": "2026-08-25T09:30:00Z"
    }
]
Authentication Error

Without authentication:

401 Unauthorized
10. Notifications APIs

Notifications are user-specific.

The Notification model contains:

user
message
created_at
is_read

Each notification belongs to a specific user.

Ticket 26 - Notifications API
Endpoint
GET /api/notifications/
Authentication

Yes.

Purpose

Returns notifications belonging only to the currently authenticated user.

Success
200 OK

Example:

[
    {
        "id": 1,
        "user": 2,
        "message": "You have been assigned a new task.",
        "created_at": "2026-08-25T10:00:00Z",
        "is_read": false
    }
]
Important Security Behavior

A user cannot simply request another user's notifications.

The queryset is filtered using:

Notification.objects.filter(
    user=self.request.user
)

Therefore, only the logged-in user's notifications are returned.

Notifications are sorted newest first:

.order_by("-created_at")
Ticket 27 - Mark Notification as Read API
Endpoint
PUT /api/notifications/{notification_id}/mark_read/
Purpose

Marks a notification as read.

Before:

{
    "id": 1,
    "message": "You have been assigned a new task.",
    "is_read": false
}

After:

{
    "id": 1,
    "message": "You have been assigned a new task.",
    "is_read": true
}
Authentication

Yes.

IsAuthenticated
Required Permission

The authenticated user can mark their own notification as read.

A user must not be able to modify another user's notification.

Request Body

No request body is required.

The notification ID is provided in the URL.

Example:

PUT /api/notifications/1/mark_read/

Header:

Authorization: Bearer <access-token>
Successful Response
200 OK

Example:

{
    "id": 1,
    "user": 2,
    "message": "You have been assigned a new task.",
    "created_at": "2026-08-25T10:00:00Z",
    "is_read": true
}
Notification Not Found
404 Not Found

This should also cover the case where the notification does not belong to the authenticated user.

Working

The API performs the following process:

Receives the notification ID.
Gets the authenticated user from the request.
Finds the notification belonging to that user.
Changes:
is_read = True
Saves the notification.
Returns the updated notification.

The important security principle is that the notification should be retrieved using both:

notification ID

and:

request.user

This prevents users from modifying notifications belonging to other users.

11. HTTP Status Codes

The API uses standard HTTP status codes.

200 OK

Request completed successfully.

Used for:

GET requests
Successful updates
Successful task assignment
Mark notification as read
201 Created

A new object was successfully created.

Used for:

User registration
Project creation
Task creation
Document upload
Comment creation
204 No Content

The requested object was successfully deleted.

Used for:

Project deletion
Task deletion
Document deletion
Comment deletion
205 Reset Content

Used by logout after successfully invalidating the refresh token.

400 Bad Request

The request contains invalid or missing data.

Examples:

Invalid serializer data
Missing required field
Invalid assignee
User is not a project member
401 Unauthorized

Authentication is missing or invalid.

Example:

Authorization header missing
Invalid JWT token
Expired access token
403 Forbidden

The user is authenticated but does not have permission.

Example:

Developer attempts to create a project
Developer attempts to delete a project
404 Not Found

The requested object does not exist or is not available to the user.

Examples:

Project does not exist
Task does not exist
Comment does not belong to current user
Notification does not belong to current user
12. Permissions

The project uses several permission classes.

AllowAny

Allows requests without authentication.

Currently used for registration.

Example:

POST /api/register/
IsAuthenticated

Requires the user to provide a valid JWT access token.

Example:

GET /api/projects/
IsManager

Custom permission used to restrict management operations to users whose profile role is:

manager

Manager-only operations include:

Create project
Update project
Delete project
Create task
Update task
Delete task
Assign task
13. Validation

Django REST Framework automatically validates serializer data.

Validation includes:

Required fields
Data types
Foreign key values
Choice fields
Email validation
File validation
Model constraints
User Validation

The email field is unique:

email = models.EmailField(unique=True)

Therefore, duplicate email addresses are rejected.

Project Validation

The project requires a title.

The dates must be valid date values.

Example:

{
    "start_date": "2026-08-25",
    "end_date": "2026-09-25"
}
Task Status Validation

Only predefined task statuses should be accepted:

open
review
working
awaiting_release
waiting_qa

An invalid status will produce a validation error.

Foreign Key Validation

For example:

{
    "project": 999
}

If project 999 does not exist, DRF returns a validation error.

Example:

{
    "project": [
        "Invalid pk \"999\" - object does not exist."
    ]
}
14. File Upload

Documents use Django's:

FileField

and profile pictures use:

ImageField

Document upload requests should use:

multipart/form-data

Example Postman form:

Key	Type	Value
name	Text	Requirements
description	Text	Project requirements
version	Text	1.0
project	Text	1
file	File	requirements.pdf
15. JWT Authentication Flow

The recommended authentication flow is:

Step 1 - Register
POST /api/register/

Example:

{
    "username": "developer",
    "email": "developer@example.com",
    "password": "StrongPassword123"
}
Step 2 - Login
POST /api/login/

Example:

{
    "username": "developer",
    "password": "StrongPassword123"
}

The server returns:

{
    "refresh": "...",
    "access": "..."
}
Step 3 - Copy Access Token

Copy the:

access

token.

Step 4 - Send Token

In Postman use:

Authorization

Type:

Bearer Token

Paste the access token.

Step 5 - Access Protected APIs

Example:

GET /api/projects/

The server checks the JWT token.

If valid:

200 OK

If missing:

401 Unauthorized
Step 6 - Refresh Access Token

When the access token expires:

POST /api/token/refresh/

Request:

{
    "refresh": "your-refresh-token"
}

Response:

{
    "access": "new-access-token"
}
Step 7 - Logout
POST /api/logout/

Request:

{
    "refresh": "your-refresh-token"
}

The refresh token is blacklisted.

16. API Testing

The project APIs were manually tested using Postman.

Testing should cover:

Authentication
Registration
Login
Logout
Project APIs
Task APIs
Task assignment
Document upload
Document update
Document deletion
Comment APIs
Timeline API
Notification API
Notification mark-as-read
Permission behavior
Validation behavior
Error responses
Authentication Testing

Test:

POST /api/register/
POST /api/login/
POST /api/logout/
POST /api/token/refresh/

Verify:

Correct credentials work.
Wrong credentials fail.
Missing token is rejected.
Logout invalidates refresh token.
Project Testing

Test:

POST /api/projects/
GET /api/projects/
GET /api/projects/{id}/
PUT /api/projects/{id}/
DELETE /api/projects/{id}/

Verify:

Manager can create projects.
Authenticated users can list projects.
Manager can update projects.
Manager can delete projects.
Unauthorized requests are rejected.
Task Testing

Test:

POST /api/tasks/
GET /api/tasks/
GET /api/tasks/{id}/
PUT /api/tasks/{id}/
DELETE /api/tasks/{id}/
POST /api/tasks/{id}/assign/

Verify:

Managers can create tasks.
Managers can update tasks.
Managers can delete tasks.
Team members can be assigned.
Non-team members cannot be assigned.
Document Testing

Test:

POST /api/documents/
GET /api/documents/list/
GET /api/documents/{id}/
PUT /api/documents/{id}/
DELETE /api/documents/{id}/

Verify:

File uploads successfully.
File metadata is saved.
Version can be updated.
Documents can be retrieved.
Documents can be deleted.
Authentication is required.
Comment Testing

Test:

POST /api/comments/
GET /api/comments/list/
GET /api/comments/{id}/
PUT /api/comments/{id}/
DELETE /api/comments/{id}/

Verify:

Authenticated user can create comments.
Author is automatically assigned.
User can update own comment.
User can delete own comment.
User cannot modify another user's comment.
Timeline Testing

Test:

GET /api/timeline/

Verify:

Authentication is required.
Timeline events are returned.
Newest events appear first.
Notification Testing

Test:

GET /api/notifications/
PUT /api/notifications/{id}/mark_read/

Verify:

Only authenticated users can access notifications.
User receives their own notifications.
Notification status changes from false to true.
Users cannot mark another user's notification as read.
17. Complete API Endpoint List
Ticket	API	Method	Authentication	Permission
1	/api/register/	POST	No	Any
2	/api/login/	POST	No	Any
3	/api/logout/	POST	Yes	Authenticated
4	/api/projects/	POST	Yes	Manager
5	/api/projects/	GET	Yes	Authenticated
6	/api/projects/{id}/	GET	Yes	Authenticated
7	/api/projects/{id}/	PUT	Yes	Manager
8	/api/projects/{id}/	DELETE	Yes	Manager
9	/api/tasks/	POST	Yes	Manager
10	/api/tasks/	GET	Yes	Authenticated
11	/api/tasks/{id}/	GET	Yes	Authenticated
12	/api/tasks/{id}/	PUT	Yes	Manager
13	/api/tasks/{id}/	DELETE	Yes	Manager
14	/api/tasks/{id}/assign/	POST	Yes	Manager
15	/api/documents/	POST	Yes	Authenticated
16	/api/documents/list/	GET	Yes	Authenticated
17	/api/documents/{id}/	GET	Yes	Authenticated
18	/api/documents/{id}/	PUT	Yes	Authenticated
19	/api/documents/{id}/	DELETE	Yes	Authenticated
20	/api/comments/	POST	Yes	Authenticated
21	/api/comments/list/	GET	Yes	Authenticated
22	/api/comments/{id}/	GET	Yes	Authenticated
23	/api/comments/{id}/	PUT	Yes	Own comment
24	/api/comments/{id}/	DELETE	Yes	Own comment
25	/api/timeline/	GET	Yes	Authenticated
26	/api/notifications/	GET	Yes	Own notifications
27	/api/notifications/{id}/mark_read/	PUT	Yes	Own notification
18. Project Working Flow

The complete application workflow is:

User Registration
       |
       v
User Login
       |
       v
JWT Access + Refresh Tokens
       |
       v
Authenticated API Requests
       |
       +-------------------+
       |                   |
       v                   v
   Manager             Developer / QA
       |                   |
       v                   |
Create Project             |
       |                   |
       v                   |
Add Team Members           |
       |                   |
       v                   |
Create Tasks               |
       |                   |
       v                   |
Assign Tasks --------------+
       |
       v
Task Work
       |
       v
Comments / Discussions
       |
       v
Documents
       |
       v
Timeline Events
       |
       v
Notifications
       |
       v
Mark Notification Read
Database Relationship Overview

The main relationships are:

User
 |
 +---- Profile (One-to-One)
 |
 +---- Created Projects
 |
 +---- Team Projects
 |
 +---- Assigned Tasks
 |
 +---- Comments
 |
 +---- Timeline Events
 |
 +---- Notifications

Project:

Project
 |
 +---- Team Members (Many-to-Many)
 |
 +---- Tasks (One-to-Many)
 |
 +---- Documents (One-to-Many)
 |
 +---- Comments (One-to-Many)
 |
 +---- Timeline Events (One-to-Many)

Task:

Task
 |
 +---- Project
 |
 +---- Assignee
 |
 +---- Comments

Document:

Document
 |
 +---- Project
 |
 +---- File
 |
 +---- Version

Comment:

Comment
 |
 +---- Author
 |
 +---- Task
 |
 +---- Project

Notification:

Notification
 |
 +---- User
Roles

The application currently supports the following profile roles:

Manager

Managers are responsible for project and task management.

Manager capabilities include:

Create projects
Update projects
Delete projects
Create tasks
Update tasks
Delete tasks
Assign tasks
Developer

Developers are project team members who can work on assigned tasks and participate in project activities according to the API permissions.

QA

QA users represent quality assurance team members.

They can participate in project workflows according to the permissions assigned by the application.

Security Considerations

The API uses authentication and permission checks for protected resources.

Important security features include:

Password hashing through Django's user system
JWT authentication
Refresh token blacklisting on logout
Authenticated-only APIs
Manager-specific permissions
User-specific notifications
User-specific comment modification
Project team-member validation during task assignment
Error Handling

The API uses standard DRF error responses.

Example:

{
    "detail": "Authentication credentials were not provided."
}

Validation errors may appear as:

{
    "project": [
        "Invalid pk \"999\" - object does not exist."
    ]
}

Custom errors may appear as:

{
    "detail": "Assignee is required."
}

or:

{
    "detail": "User is not a member of this project."
}
API Development Architecture

The application follows Django REST Framework's layered architecture.

Models

Models define the database structure.

Main models:

User
Profile
Project
Task
Document
Comment
TimelineEvent
Notification
Serializers

Serializers convert Django model objects into JSON responses and validate incoming API data.

Main serializers:

UserSerializer
ProfileSerializer
ProjectSerializer
TaskSerializer
DocumentSerializer
CommentSerializer
TimelineEventSerializer
NotificationSerializer
Views

The project primarily uses DRF generic API views.

Examples:

CreateAPIView
ListAPIView
ListCreateAPIView
RetrieveUpdateDestroyAPIView
GenericAPIView

This reduces repeated code and provides standard REST behavior.

URLs

API routes are defined in:

core/urls.py

The main project URL configuration includes:

/api/

through:

path("api/", include("core.urls"))
Media Files

Uploaded documents and profile pictures are stored using Django's media configuration.

During development, media URLs are served through Django's development configuration.

The project uses:

MEDIA_URL
MEDIA_ROOT
Final API Verification Checklist

Before considering the project complete, verify:

 User registration works
 User login works
 User logout works
 JWT authentication works
 Project creation works
 Project listing works
 Project detail works
 Project update works
 Project deletion works
 Task creation works
 Task listing works
 Task detail works
 Task update works
 Task deletion works
 Task assignment works
 Team-member validation works
 Document upload works
 Document listing works
 Document detail works
 Document update works
 Document deletion works
 Comment creation works
 Comment listing works
 Comment detail works
 Own comment update works
 Own comment deletion works
 Other user's comments are protected
 Timeline API works
 Notifications API works
 Notification mark-as-read works
 Authentication permissions verified
 Validation verified
 File upload verified
 API tests completed
 Django system check completed
 Migrations verified
 Debug print statements checked
 TODO/FIXME comments checked
Conclusion

The Collaborative Project Management API provides a complete backend system for collaborative project development.

The API supports:

Authentication
      +
User Management
      +
Profiles
      +
Project Management
      +
Task Management
      +
Task Assignment
      +
Document Management
      +
Comments
      +
Timeline Events
      +
Notifications