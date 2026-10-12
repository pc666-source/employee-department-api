
from datetime import date

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Department, Employee


class DepartmentAPITests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name="IT")
        self.url = "/api/departments/"

    def test_create_department(self):
        response = self.client.post(
            self.url,
            {"name": "HR"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Department.objects.filter(name="HR").exists()
        )

    def test_list_departments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], "IT")

    def test_retrieve_department(self):
        response = self.client.get(
            f"{self.url}{self.department.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "IT")

    def test_update_department(self):
        response = self.client.patch(
            f"{self.url}{self.department.id}/",
            {"name": "Technology"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, "Technology")

    def test_delete_department(self):
        response = self.client.delete(
            f"{self.url}{self.department.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Department.objects.filter(pk=self.department.id).exists()
        )

    def test_missing_department_returns_404(self):
        response = self.client.get(f"{self.url}9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EmployeeAPITests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name="IT")
        self.url = "/api/employees/"
        self.employee_data = {
            "name": "Anil",
            "email": "anil@example.com",
            "salary": "34000.00",
            "department": self.department.id,
            "joining_date": "2023-09-21",
        }

    def create_employee(self, **overrides):
        data = {**self.employee_data, **overrides}
        return Employee.objects.create(
            name=data["name"],
            email=data["email"],
            salary=data["salary"],
            department=self.department,
            joining_date=date.fromisoformat(data["joining_date"]),
        )

    def test_create_employee(self):
        response = self.client.post(
            self.url,
            self.employee_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Employee.objects.filter(email="anil@example.com").exists()
        )

    def test_list_employees_is_paginated(self):
        self.create_employee()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_employee(self):
        employee = self.create_employee()
        response = self.client.get(f"{self.url}{employee.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], employee.email)

    def test_update_employee(self):
        employee = self.create_employee()
        response = self.client.patch(
            f"{self.url}{employee.id}/",
            {"name": "Anil Kumar"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.name, "Anil Kumar")

    def test_delete_employee(self):
        employee = self.create_employee()
        response = self.client.delete(f"{self.url}{employee.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Employee.objects.filter(pk=employee.id).exists()
        )

    def test_duplicate_email_is_rejected(self):
        self.create_employee()

        duplicate = {
            **self.employee_data,
            "name": "Another Employee",
        }
        response = self.client.post(
            self.url, duplicate, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_invalid_email_is_rejected(self):
        response = self.client.post(
            self.url,
            {**self.employee_data, "email": "not-an-email"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_nonexistent_department_is_rejected(self):
        response = self.client.post(
            self.url,
            {**self.employee_data, "department": 9999},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("department", response.data)

    def test_missing_employee_returns_404(self):
        response = self.client.get(f"{self.url}9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_by_name(self):
        self.create_employee()
        self.create_employee(
            name="Priya",
            email="priya@example.com",
        )

        response = self.client.get(f"{self.url}?search=Anil")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Anil")

    def test_filter_by_department(self):
        self.create_employee()

        hr = Department.objects.create(name="HR")
        Employee.objects.create(
            name="Priya",
            email="priya@example.com",
            salary="45000.00",
            department=hr,
            joining_date=date(2024, 6, 15),
        )

        response = self.client.get(
            f"{self.url}?department={self.department.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Anil")
