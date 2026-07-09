from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'department', 'department_name',
            'role', 'phone', 'joining_date'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=['employee', 'manager', 'admin'],
        default='employee'
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'password2', 'role', 'department'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        role = validated_data.pop('role', 'employee')
        department = validated_data.pop('department', None)
        validated_data.pop('password2')

        user = User.objects.create_user(**validated_data)

        Employee.objects.create(
            user=user,
            role=role,
            department=department
        )
        return user