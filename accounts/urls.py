from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, ProfileView, DepartmentListView, EmployeeListView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),
    # Departments & Employees
    path('departments/', DepartmentListView.as_view(), name='departments'),
    path('employees/', EmployeeListView.as_view(), name='employees'),
]