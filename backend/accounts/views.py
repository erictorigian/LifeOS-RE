"""
Django authentication views for login/logout/signup.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignUpForm


def login_view(request):
    """Django login view"""
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
                next_url = request.GET.get('next', 'crm:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def signup_view(request):
    """Django signup view"""
    if request.user.is_authenticated:
        return redirect('crm:dashboard')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.get_full_name() or user.email}!')
            return redirect('crm:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def logout_view(request):
    """Django logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

