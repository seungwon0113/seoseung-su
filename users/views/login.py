from typing import cast

from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from users.forms.login import LoginForm
from users.models import User


class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        user = cast(User, request.user)
        if user.is_authenticated:
            return redirect('home')
        form = LoginForm()
        context = {'form': form}
        return render(request, 'users/login.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LoginForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            # 실제 로그인 로직 추가
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # URL name 사용
            else:
                form.add_error(None, '유효하지 않은 사용자명 또는 비밀번호입니다.')

        return render(request, 'users/login.html', context)