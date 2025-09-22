import json

from django.contrib.auth import login
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from users.services.social_login import GoogleLoginService


@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(View):
    """Google 소셜 로그인 처리 뷰"""
    
    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)
            credential = data.get('credential')
            
            if not credential:
                return JsonResponse({
                    'success': False,
                    'message': 'Google 인증 정보가 없습니다.'
                }, status=400)
            
            # Google 로그인 서비스로 인증 처리
            user, error = GoogleLoginService.authenticate_user(credential)
            
            if error:
                return JsonResponse({
                    'success': False,
                    'message': error
                }, status=400)
            
            if user:
                # 사용자 로그인
                login(request, user)
                
                # 리다이렉트 URL 결정 (홈페이지로 고정)
                next_url = request.GET.get('next', '/')
                
                return JsonResponse({
                    'success': True,
                    'message': 'Google 로그인에 성공했습니다. 홈페이지로 이동합니다.',
                    'redirect_url': next_url,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': user.role
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': '사용자 인증에 실패했습니다.'
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': '잘못된 JSON 형식입니다.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'서버 오류가 발생했습니다: {str(e)}'
            }, status=500)