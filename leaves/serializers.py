from rest_framework import serializers
from .models import LeaveRequest
from accounts.serializers import EmployeeSerializer


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.user.get_full_name',
        read_only=True
    )
    reviewed_by_name = serializers.CharField(
        source='reviewed_by.user.get_full_name',
        read_only=True
    )
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name',
            'leave_type', 'start_date', 'end_date',
            'total_days', 'reason', 'status',
            'reviewed_by', 'reviewed_by_name',
            'reviewed_at', 'created_at'
        ]
        read_only_fields = ['status', 'reviewed_by', 'reviewed_at', 'created_at']


class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'reason']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(
                "Start date cannot be after end date"
            )
        return data


class LeaveStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['status']

    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError(
                "Status must be approved or rejected"
            )
        return value