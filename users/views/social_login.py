import json

from django.contrib.auth import login
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from users.services.social_login import GoogleLoginService, KakaoLoginService


@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(View):
    
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
                
                # 필수 동의 항목 체크
                if not user.terms_of_use or not user.personal_info_consent:
                    return JsonResponse({
                        'success': True,
                        'message': 'Google 로그인에 성공했습니다. 동의 항목을 확인해주세요.',
                        'redirect_url': '/users/consent/',
                        'requires_consent': True,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'role': user.role
                        }
                    })
                
                # 안전한 리다이렉트 URL 결정 (오픈 리디렉션 취약점 방지)
                next_url = request.GET.get('next', '/')
                if not url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                ):
                    next_url = '/'  # 안전하지 않은 URL은 홈페이지로 리다이렉트
                
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


@method_decorator(csrf_exempt, name='dispatch')
class KakaoLoginView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            # JSON 데이터 파싱
            data = json.loads(request.body)
            access_token = data.get('access_token')
            
            if not access_token:
                return JsonResponse({
                    'success': False,
                    'message': '카카오 액세스 토큰이 없습니다.'
                }, status=400)
            
            # 카카오 로그인 서비스로 인증 처리
            user, error = KakaoLoginService.authenticate_user(access_token)
            
            if error:
                return JsonResponse({
                    'success': False,
                    'message': error
                }, status=400)
            
            if user:
                # 사용자 로그인
                login(request, user)
                
                # 필수 동의 항목 체크
                if not user.terms_of_use or not user.personal_info_consent:
                    return JsonResponse({
                        'success': True,
                        'message': '카카오 로그인에 성공했습니다. 동의 항목을 확인해주세요.',
                        'redirect_url': '/users/consent/',
                        'requires_consent': True,
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'role': user.role
                        }
                    })
                
                # 안전한 리다이렉트 URL 결정 (오픈 리디렉션 취약점 방지)
                next_url = request.GET.get('next', '/')
                if not url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure()
                ):
                    next_url = '/'  # 안전하지 않은 URL은 홈페이지로 리다이렉트
                
                return JsonResponse({
                    'success': True,
                    'message': '카카오 로그인에 성공했습니다. 홈페이지로 이동합니다.',
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