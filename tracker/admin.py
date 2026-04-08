from django.contrib import admin
from .models import UserProfile, Expense


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'income', 'limit')
    search_fields = ('user__username',)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'description', 'amount', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('description', 'user__username')
    ordering = ('-created_at',)