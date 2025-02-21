# users\views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Замените 'home' на URL вашей главной страницы
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Неверные учетные данные'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Неверная форма'})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматически входит пользователя после регистрации
            return redirect('home')  # Замените 'home' на URL вашей главной страницы
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home') # Замените 'login' на URL вашей страницы входа

# @login_required
def home_view(request):
    return render(request, 'home.html')