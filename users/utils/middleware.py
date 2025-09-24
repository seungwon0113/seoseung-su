from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from typing import Callable

from users.models import User


class ConsentRequiredMiddleware:
    """
    소셜 로그인 후 필수 동의 항목이 완료되지 않은 사용자를 동의 페이지로 리다이렉트하는 미들웨어
    """
    
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        # 동의 페이지 관련 URL들은 체크하지 않음
        exempt_urls = [
            '/users/',
            '/users/login/',
            '/users/signup/',
            '/users/google-login/',
            '/users/kakao-login/',
            '/admin/',
            '/static/',
            '/media/',
            '/products/*'
        ]
        
        # 현재 URL이 exempt_urls에 포함되는지 체크
        if any(request.path.startswith(url) for url in exempt_urls):
            return self.get_response(request)
        
        # 로그인된 사용자인지 체크
        if request.user.is_authenticated and isinstance(request.user, User):
            # 필수 동의 항목이 완료되지 않은 경우
            if not request.user.terms_of_use or not request.user.personal_info_consent:
                return redirect(reverse('consent'))
        
        return self.get_response(request)
