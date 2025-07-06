from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from scraping_project import settings








class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'app_auth/homepage.html'
    
    
def login_view(request):
    print("login_view called, method:", request.method)
    
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'app_auth/login.html')


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
