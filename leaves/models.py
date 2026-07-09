from django.db import models 
from accounts.models import Employee

class LeaveRequest(models.Model):

    LEAVE_TYPE_CHOICES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('emergency', 'Emergency Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete = models.CASCADE,
        related_name = 'leave_requests'
    )
    leave_type = models.CharField(
        max_length = 20,
        choices = LEAVE_TYPE_CHOICES,
        default = 'annual'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'pending'
    )
    reviewed_by = models.ForeignKey(
        Employee,
        on_delete = models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'reviewed_leaves'
    )
    reviewed_at = models.DateTimeField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type} ({self.status})"
    
    @property
    def total_days(self):
        delta = self.end_date - self.start_date
        return delta.days + 1
