from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense, UserProfile


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = ""

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        print("LOGIN POST:", request.POST)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password."

    return render(request, 'tracker/login_only.html', {'error': error})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    error = ""

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        print("SIGNUP POST:", request.POST)

        if username == "" or password1 == "" or password2 == "":
            error = "All fields are required."
        elif password1 != password2:
            error = "Passwords do not match."
        elif len(password1) < 8:
            error = "Password must be at least 8 characters."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        else:
            user = User.objects.create_user(username=username, password=password1)
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('dashboard')

    return render(request, 'tracker/signup_only.html', {'error': error})


@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        print("DASHBOARD POST:", request.POST)

        if request.POST.get('action') == 'set_income':
            profile.income = float(request.POST.get('income', 0))
            profile.limit = float(request.POST.get('limit', 0))
            profile.save()
            return redirect('dashboard')

        elif request.POST.get('action') == 'add_expense':
            Expense.objects.create(
                user=request.user,
                category=request.POST.get('category'),
                description=request.POST.get('description'),
                amount=float(request.POST.get('amount', 0))
            )
            return redirect('dashboard')

    expenses = Expense.objects.filter(user=request.user).order_by('-created_at')
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    remaining = profile.income - total
    category_data = expenses.values('category').annotate(total=Sum('amount')).order_by('category')

    warning = None
    if profile.limit > 0 and total > profile.limit:
        warning = "Warning: Your total expenses have exceeded your expense limit!"

    return render(request, 'tracker/dashboard.html', {
        'profile': profile,
        'expenses': expenses,
        'total': total,
        'remaining': remaining,
        'category_data': category_data,
        'warning': warning
    })


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    return redirect('dashboard')


def logout_view(request):
    logout(request)
    return redirect('home')