from typing import cast

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from users.forms.signup import SignupForm
from users.models import User
from users.services.user_signup import UserService


class SignupView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = cast(User, request.user)
        form = SignupForm()
        if user.is_authenticated:
            return redirect('home')
        context = {'form': form}
        return render(request, 'users/signup.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                UserService.create_and_login_user(request, form.cleaned_data)
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
        context = {'form': form}
        return render(request, 'users/signup.html', context)

