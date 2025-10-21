from typing import cast

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from inquire.forms.inqurie_create import InquireForm
from inquire.services.inquire_user_valid import InquireUserValidService
from users.models import User


class InquireView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = cast(User, InquireForm(user=request.user))
        context = {'form': form}
        return render(request, 'inquire/inquire.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = InquireForm(request.POST, user=request.user)
        
        if not form.is_valid():
            messages.error(request, '입력 정보를 다시 확인해주세요.')
            return render(request, 'inquire/inquire.html', {'form': form})
        
        data = form.cleaned_data
        user, email = InquireUserValidService.validate_inquire_user_valid(request.user)

        if not email:
            if 'email' in data:
                email = data['email']
            else:
                email = request.user.email if request.user.is_authenticated else None

        if not email:
            messages.error(request, '이메일 주소를 입력해주세요.')
            return render(request, 'inquire/inquire.html', {'form': form})

        success, message = InquireUserValidService.process_inquire(
            user=user,
            email=email,
            title=data['title'],
            content=data['content'],
            item=data['item']
        )
        
        if success:
            messages.success(request, message)
            return redirect('inquire_success')
        else:
            messages.error(request, message)
            return render(request, 'inquire/inquire.html', {'form': form})


class InquireSuccessView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'inquire/inquire_success.html')