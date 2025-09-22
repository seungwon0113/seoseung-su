from django.http import HttpRequest, JsonResponse
from django.views import View

from users.models import User


class CheckDuplicateView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        username = request.GET.get('username', '').strip()
        email = request.GET.get('email', '').strip()
        
        result = {
            'username': {
                'available': True,
                'message': ''
            },
            'email': {
                'available': True,
                'message': ''
            }
        }
        
        if username:
            if User.objects.filter(username=username).exists():
                result['username'] = {
                    'available': False,
                    'message': '이미 존재하는 아이디입니다.'
                }
            else:
                result['username'] = {
                    'available': True,
                    'message': '사용 가능한 아이디입니다.'
                }
        
        if email:
            if User.objects.filter(email=email).exists():
                result['email'] = {
                    'available': False,
                    'message': '이미 가입된 이메일입니다.'
                }
            else:
                result['email'] = {
                    'available': True,
                    'message': '사용 가능한 이메일입니다.'
                }
        
        return JsonResponse(result)
