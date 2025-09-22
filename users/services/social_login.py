
from typing import Any, Dict, Optional, Tuple, cast

from django.conf import settings
from django.db import transaction
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from users.models import User


class GoogleLoginService:

    @staticmethod
    def _generate_unique_username(email: str) -> str:
        """이메일에서 유니크한 사용자명 생성"""
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
            
        return username

    @staticmethod
    def verify_google_token(credential: str) -> Optional[Dict[str, Any]]:
        try:
            # Google 공식 라이브러리를 사용한 토큰 검증
            request = google_requests.Request()  # type: ignore
            idinfo = cast(Dict[str, Any], id_token.verify_oauth2_token(  # type: ignore
                credential, 
                request, 
                settings.GOOGLE_OAUTH2_CLIENT_ID
            ))
            
            # 토큰이 유효한지 확인
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
                
            return idinfo
        except ValueError as e:
            print(f"Google token verification error: {e}")
            return None
        except Exception as e:
            print(f"Google token verification error: {e}")
            return None
    
    @staticmethod
    def get_or_create_user(google_user_info: Dict[str, Any]) -> User:
        """Google 사용자 정보로 사용자 생성 또는 조회"""
        try:
            google_id = google_user_info.get('sub')
            email = google_user_info.get('email')
            name = google_user_info.get('name', '')
            picture = google_user_info.get('picture', '')
            
            if not google_id or not email:
                raise ValueError("Google 사용자 정보가 없습니다.")
            
            # 원자적 사용자 조회/생성 (경쟁 상태 방지)
            with transaction.atomic():
                # 1. Google ID로 기존 사용자 조회
                try:
                    user = User.objects.get(google_id=google_id)
                    return user
                except User.DoesNotExist:
                    pass
                
                # 2. 이메일로 기존 사용자 조회 및 Google ID 추가
                try:
                    user = User.objects.select_for_update().get(email=email)
                    user.google_id = google_id
                    user.save()
                    return user
                except User.DoesNotExist:
                    pass
                
                # 3. 새 사용자 생성
                username = GoogleLoginService._generate_unique_username(email)
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=None,  # 소셜 로그인은 비밀번호 없음
                    google_id=google_id,
                    first_name=name.split(' ')[0] if name else '',
                    last_name=' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else '',
                    profile_image=picture,
                    is_active=True,
                    # 기본 동의 항목들
                    terms_of_use=True,
                    personal_info_consent=True,
                    sns_consent_to_receive=False,
                    email_consent_to_receive=False
                )
            
            return user
        except Exception as e:
            print(f"User creation/retrieval error: {e}")
            raise ValueError(f"사용자 생성/조회 중 오류가 발생했습니다: {str(e)}")
    
    @classmethod
    def authenticate_user(cls, credential: str) -> Tuple[Optional[User], Optional[str]]:
        """Google 로그인 인증 처리"""
        try:
            # 1. Google 토큰 검증
            google_user_info = cls.verify_google_token(credential)
            if not google_user_info:
                return None, "Google 토큰 검증에 실패했습니다."
            
            # 2. 사용자 생성 또는 조회
            user = cls.get_or_create_user(google_user_info)
            if not user:
                return None, "사용자 생성/조회에 실패했습니다."
            
            return user, None
        except Exception as e:
            return None, str(e)
