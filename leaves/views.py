from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import LeaveRequest
from .serializers import (
    LeaveRequestSerializer,
    LeaveRequestCreateSerializer,
    LeaveStatusUpdateSerializer
)


class LeaveRequestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response(
                {'error': 'Employee profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Admin/Manager sees all leaves, Employee sees only their own
        if employee.role in ['admin', 'manager']:
            leaves = LeaveRequest.objects.all()
        else:
            leaves = LeaveRequest.objects.filter(employee=employee)

        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data)


class LeaveRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response(
                {'error': 'Employee profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeaveRequestCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(
                {'message': 'Leave request submitted successfully',
                 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LeaveRequestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, employee):
        try:
            leave = LeaveRequest.objects.get(pk=pk)
            # Employee can only view their own leaves
            if employee.role == 'employee' and leave.employee != employee:
                return None, Response(
                    {'error': 'Permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            return leave, None
        except LeaveRequest.DoesNotExist:
            return None, Response(
                {'error': 'Leave request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response(
                {'error': 'Employee profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        leave, error = self.get_object(pk, employee)
        if error:
            return error
        serializer = LeaveRequestSerializer(leave)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response(
                {'error': 'Employee profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        leave, error = self.get_object(pk, employee)
        if error:
            return error
        if leave.status != 'pending':
            return Response(
                {'error': 'Only pending leaves can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        leave.delete()
        return Response(
            {'message': 'Leave request cancelled successfully'},
            status=status.HTTP_200_OK
        )


class LeaveStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            employee = request.user.employee_profile
        except Exception:
            return Response(
                {'error': 'Employee profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Only manager and admin can approve/reject
        if employee.role not in ['manager', 'admin']:
            return Response(
                {'error': 'Only managers and admins can update leave status'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            leave = LeaveRequest.objects.get(pk=pk)
        except LeaveRequest.DoesNotExist:
            return Response(
                {'error': 'Leave request not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = LeaveStatusUpdateSerializer(
            leave,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(
                reviewed_by=employee,
                reviewed_at=timezone.now()
            )
            return Response({
                'message': f'Leave request {leave.status} successfully',
                'data': LeaveRequestSerializer(leave).data
            })
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )