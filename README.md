**# Employee Leave Management System**



**A production-ready REST API built with Django and Django REST Framework for managing employee leave requests with JWT authentication and role-based access control.**



**## Tech Stack**



**- \*\*Backend:\*\* Python, Django 6.0, Django REST Framework**

**- \*\*Authentication:\*\* JWT (SimpleJWT)**

**- \*\*Database:\*\* SQLite (development)**

**- \*\*Tools:\*\* Postman, Git**



**## Features**



**- JWT Authentication (register, login, logout, token refresh)**

**- Role-Based Access Control (Employee, Manager, Admin)**

**- Leave application workflow (apply, approve, reject, cancel)**

**- Manager dashboard — view and manage team leave requests**

**- Auto-calculated leave duration via @property**

**- Django Admin panel for data management**



**## API Endpoints**



**### Authentication**

**| Method | Endpoint | Description | Auth |**

**|--------|----------|-------------|------|**

**| POST | /api/accounts/register/ | Register new user | No |**

**| POST | /api/accounts/login/ | Login and get JWT token | No |**

**| POST | /api/accounts/logout/ | Logout and blacklist token | Yes |**

**| POST | /api/accounts/token/refresh/ | Refresh access token | No |**



**### Profile \& Users**

**| Method | Endpoint | Description | Auth |**

**|--------|----------|-------------|------|**

**| GET | /api/accounts/profile/ | View own profile | Yes |**

**| PUT | /api/accounts/profile/ | Update own profile | Yes |**

**| GET | /api/accounts/employees/ | List all employees | Yes |**

**| GET | /api/accounts/departments/ | List all departments | Yes |**



**### Leave Management**

**| Method | Endpoint | Description | Auth |**

**|--------|----------|-------------|------|**

**| GET | /api/leaves/ | List leaves (own or all) | Yes |**

**| POST | /api/leaves/apply/ | Apply for leave | Yes |**

**| GET | /api/leaves/{id}/ | View leave detail | Yes |**

**| DELETE | /api/leaves/{id}/ | Cancel leave request | Yes |**

**| PATCH | /api/leaves/{id}/status/ | Approve/Reject leave | Manager/Admin |**



**## Setup Instructions**



**```bash**

**# Clone the repo**

**git clone https://github.com/santoshpatel2001srp/employee-leave-management.git**

**cd employee-leave-management**



**# Create virtual environment**

**python -m venv env**

**env\\Scripts\\activate  # Windows**



**# Install dependencies**

**pip install -r requirements.txt**



**# Run migrations**

**python manage.py migrate**



**# Create superuser**

**python manage.py createsuperuser**



**# Start server**

**python manage.py runserver**

**```**



**## Role-Based Access**



**| Role | Permissions |**

**|------|-------------|**

**| Employee | Apply, view own leaves, cancel pending leaves |**

**| Manager | All employee permissions + approve/reject any leave |**

**| Admin | Full access to all resources |**



**## Project Structure**

