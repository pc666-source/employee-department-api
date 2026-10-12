# Employee & Department REST API

## Project Overview

This project is a database-backed REST API developed using Django and Django REST Framework. It manages employees and departments, allowing users to create, retrieve, update, delete, search, and filter records.

## Features

- CRUD operations for departments and employees
- Relationship between employees and departments
- Email format validation
- Prevention of duplicate employee email addresses
- Department-based employee filtering
- Employee search by name
- Pagination of employee records
- Proper handling of missing records
- SQLite database
- REST API browsable interface

## Technologies Used

- Python
- Django
- Django REST Framework
- django-filter
- SQLite
- Git and GitHub

## Project Structure

```text
employee_department_api/
├── api/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── config/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Models

### Department

- `id`: Automatically generated primary key
- `name`: Department name

### Employee

- `id`: Automatically generated primary key
- `name`: Employee name
- `email`: Unique email address
- `salary`: Employee salary
- `department`: Foreign key referencing a department
- `joining_date`: Employee joining date

One department can have multiple employees. Each employee belongs to one department.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd employee_department_api
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

### Department APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/departments/` | List departments |
| POST | `/api/departments/` | Create a department |
| GET | `/api/departments/{id}/` | Retrieve a department |
| PUT | `/api/departments/{id}/` | Update a department |
| PATCH | `/api/departments/{id}/` | Partially update a department |
| DELETE | `/api/departments/{id}/` | Delete a department |

### Employee APIs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/employees/` | List employees |
| POST | `/api/employees/` | Create an employee |
| GET | `/api/employees/{id}/` | Retrieve an employee |
| PUT | `/api/employees/{id}/` | Update an employee |
| PATCH | `/api/employees/{id}/` | Partially update an employee |
| DELETE | `/api/employees/{id}/` | Delete an employee |

## Example Requests

### Create a department

POST `/api/departments/`

```json
{
  "name": "IT"
}
```

### Create an employee

POST `/api/employees/`

```json
{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "salary": "45000.00",
  "department": 1,
  "joining_date": "2026-10-12"
}
```

The department ID must correspond to an existing department.

## Search, Filtering and Pagination

### Search employees by name

`GET /api/employees/?search=Rahul`

### Filter employees by department

`GET /api/employees/?department=1`

### Pagination

`GET /api/employees/?page=1`

The employee list returns paginated results with a count and navigation links.

## Validation and Error Handling

- Invalid email addresses are rejected.
- Duplicate employee email addresses are rejected.
- Missing employee or department records return a not-found response.
- Employees cannot reference a nonexistent department.
- Departments with existing employees cannot be deleted while those relationships remain.

## Running Tests

Run Django's system check:

```bash
python manage.py check
```

Run the automated test suite:

```bash
python manage.py test
```

## Future Improvements

- Automated unit and API tests
- Authentication and permissions
- Deployment to a production server
- Additional filtering and reporting features

## Author

PC
## Development Status

The project includes Department and Employee models,
REST API serializers, CRUD endpoints, email validation,
department filtering, and employee search.

Pagination is configured using Django REST Framework.
## API Usage Examples

- List employees: `GET /api/employees/`
- Create an employee: `POST /api/employees/`
- Search employees: `GET /api/employees/?search=anil`
- Filter by department: `GET /api/employees/?department=1`
- List departments: `GET /api/departments/`