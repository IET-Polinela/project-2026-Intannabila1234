from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .form import RegisterForm


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Selamat datang, {user.username}!')
            return redirect('dashboard:dashboard')
        messages.error(request, 'Username atau password salah.')
    return render(request, 'login.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('login')
    return render(request, 'register.html', {'form': form})
