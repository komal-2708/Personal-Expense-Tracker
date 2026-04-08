from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('logout/', views.logout_view, name='logout'),
]