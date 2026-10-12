from rest_framework import serializers
from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id',
            'name',
            'email',
            'salary',
            'department',
            'department_name',
            'joining_date',
        ]

    def validate_email(self, value):
        value = value.strip().lower()

        queryset = Employee.objects.filter(email__iexact=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "An employee with this email already exists."
            )

        return value