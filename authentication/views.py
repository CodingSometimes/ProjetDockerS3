from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class LoginUser(LoginView):
    template_name = 'authentication/login.html'
    next_page = reverse_lazy('blog:blog_index')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('blog:blog_index')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:blog_index')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

