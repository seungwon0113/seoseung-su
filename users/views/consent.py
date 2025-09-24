from typing import cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from users.models import User


@login_required
@require_http_methods(["GET", "POST"])
def consent_view(request: HttpRequest) -> HttpResponse:
    user = cast(User, request.user)
    
    if request.method == "GET":
        # 이미 모든 필수 동의를 완료한 경우 홈페이지로 리다이렉트
        if user.terms_of_use and user.personal_info_consent:
            return redirect('/')
        
        return render(request, 'users/consent.html', {
            'user': user
        })
    
    elif request.method == "POST":
        # 동의 항목 처리
        terms_of_use = request.POST.get('terms_of_use') == 'on'
        personal_info_consent = request.POST.get('personal_info_consent') == 'on'
        sns_consent_to_receive = request.POST.get('sns_consent_to_receive') == 'on'
        email_consent_to_receive = request.POST.get('email_consent_to_receive') == 'on'
        
        # 필수 동의 항목 체크
        if not terms_of_use or not personal_info_consent:
            messages.error(request, '필수 동의 동의 항목에 모두 동의해주세요.')
            return render(request, 'users/consent.html', {
                'user': user
            })
        
        # 사용자 동의 정보 업데이트
        user.terms_of_use = terms_of_use
        user.personal_info_consent = personal_info_consent
        user.sns_consent_to_receive = sns_consent_to_receive
        user.email_consent_to_receive = email_consent_to_receive
        user.save()
        
        return redirect('/')
    
    # 이론적으로는 도달할 수 없지만 mypy를 위해 추가
    return redirect('/')
