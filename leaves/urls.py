from django.urls import path
from .views import (
    LeaveRequestListView,
    LeaveRequestCreateView,
    LeaveRequestDetailView,
    LeaveStatusUpdateView
)

urlpatterns = [
    path('', LeaveRequestListView.as_view(), name='leave-list'),
    path('apply/', LeaveRequestCreateView.as_view(), name='leave-apply'),
    path('<int:pk>/', LeaveRequestDetailView.as_view(), name='leave-detail'),
    path('<int:pk>/status/', LeaveStatusUpdateView.as_view(), name='leave-status'),
]