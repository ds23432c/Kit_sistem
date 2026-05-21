from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import User
from .forms import LoginForm, UserCreateForm, UserEditForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(request,
                            username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def user_list(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    users = User.objects.all().order_by('role', 'last_name')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
def user_create(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    form = UserCreateForm(request.POST or None)
    generated_password = None
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        generated_password = get_random_string(10)
        user.set_password(generated_password)
        user.save()
        form.save_m2m()
        messages.success(request, f'Пользователь создан. Пароль: {generated_password}')
        return render(request, 'accounts/user_created.html', {
            'new_user': user, 'password': generated_password
        })
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Создать пользователя'})


@login_required
def user_edit(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Пользователь обновлён')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Редактировать пользователя'})


@login_required
def user_toggle_active(request, pk):
    if not request.user.is_admin:
        return redirect('dashboard')
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_list')
