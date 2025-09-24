import json
from typing import TYPE_CHECKING, Any
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from users.services.social_login import GoogleLoginService, KakaoLoginService

if TYPE_CHECKING:
    from users.models import User

User = get_user_model()  # type: ignore

@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def google_login_url() -> str:
    return reverse('google-login')


@pytest.fixture
def test_user() -> 'User':
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        personal_info_consent=True,
        terms_of_use=True
    )


class TestGoogleLoginView:
    
    def test_google_login_missing_credential(self, client: Client, google_login_url: str) -> None:
        response = client.post(
            google_login_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == 'Google 인증 정보가 없습니다.'
    
    def test_google_login_invalid_json(self, client: Client, google_login_url: str) -> None:
        response = client.post(
            google_login_url,
            data="invalid json",
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '잘못된 JSON 형식입니다.'
    

    @pytest.mark.django_db
    @patch('users.services.social_login.GoogleLoginService.authenticate_user')
    def test_google_login_authentication_failure(self, mock_authenticate: Any, client: Client, google_login_url: str) -> None:
        mock_authenticate.return_value = (None, "토큰 검증 실패")
        
        response = client.post(
            google_login_url,
            data=json.dumps({'credential': 'fake_credential'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '토큰 검증 실패'
    

    @pytest.mark.django_db
    @patch('users.services.social_login.GoogleLoginService.authenticate_user')
    def test_google_login_success(self, mock_authenticate: Any, client: Client, google_login_url: str, test_user: 'User') -> None:
        mock_authenticate.return_value = (test_user, None)
        
        response = client.post(
            google_login_url,
            data=json.dumps({'credential': 'valid_credential'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success']
        assert data['message'] == 'Google 로그인에 성공했습니다. 홈페이지로 이동합니다.'
        assert data['redirect_url'] == '/'
        assert data['user']['id'] == test_user.id
        assert data['user']['username'] == test_user.username
    

    @pytest.mark.django_db
    @patch('users.services.social_login.GoogleLoginService.authenticate_user')
    def test_google_login_with_next_parameter(self, mock_authenticate: Any, client: Client, google_login_url: str, test_user: 'User') -> None:
        mock_authenticate.return_value = (test_user, None)
        
        response = client.post(
            f"{google_login_url}?next=/profile/",
            data=json.dumps({'credential': 'valid_credential'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success']
        assert data['redirect_url'] == '/profile/'
    

    @pytest.mark.django_db
    @patch('users.services.social_login.GoogleLoginService.authenticate_user')
    def test_google_login_with_unsafe_next_parameter(self, mock_authenticate: Any, client: Client, google_login_url: str, test_user: 'User') -> None:
        mock_authenticate.return_value = (test_user, None)
        
        response = client.post(
            f"{google_login_url}?next=https://evil.com/",
            data=json.dumps({'credential': 'valid_credential'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['success']
        assert data['redirect_url'] == '/'
    
    @pytest.mark.django_db
    @patch('users.services.social_login.GoogleLoginService.authenticate_user')
    def test_google_login_user_authentication_failure(self, mock_authenticate: Any, client: Client, google_login_url: str) -> None:
        """Google 로그인 - 사용자 인증 실패 (user가 None인 경우)"""
        mock_authenticate.return_value = (None, None)  # user가 None인 경우
        
        response = client.post(
            google_login_url,
            data=json.dumps({'credential': 'valid_credential'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '사용자 인증에 실패했습니다.'
    
    @pytest.mark.django_db
    @patch('users.services.social_login.GoogleLoginService.authenticate_user')
    def test_google_login_server_error(self, mock_authenticate: Any, client: Client, google_login_url: str) -> None:
        """Google 로그인 - 서버 오류"""
        mock_authenticate.side_effect = Exception("서버 내부 오류")
        
        response = client.post(
            google_login_url,
            data=json.dumps({'credential': 'valid_credential'}),
            content_type='application/json'
        )
        
        assert response.status_code == 500
        data = response.json()
        assert not data['success']
        assert '서버 오류가 발생했습니다' in data['message']


class TestSocialLoginService:
    
    @pytest.mark.django_db
    def test_google_generate_unique_username(self) -> None:
        # 기존 사용자가 없는 경우
        username = GoogleLoginService._generate_unique_username('test@example.com')
        assert username == 'test'
        
        # 기존 사용자가 있는 경우
        User.objects.create_user(
            username='test', 
            email='existing@example.com',
            personal_info_consent=True,
            terms_of_use=True
        )
        username = GoogleLoginService._generate_unique_username('test@example.com')
        assert username == 'test_1'
        
        # 여러 기존 사용자가 있는 경우
        User.objects.create_user(
            username='test_1', 
            email='existing2@example.com',
            personal_info_consent=True,
            terms_of_use=True
        )
        username = GoogleLoginService._generate_unique_username('test@example.com')
        assert username == 'test_2'
    
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_verify_token_success(self, mock_verify: Any) -> None:
        mock_verify.return_value = {
            'iss': 'accounts.google.com',
            'sub': '12345',
            'email': 'test@example.com',
            'name': 'Test User',
            'picture': 'https://example.com/picture.jpg'
        }
        
        result = GoogleLoginService.verify_google_token('valid_token')
        
        assert result is not None
        assert result['sub'] == '12345'
        assert result['email'] == 'test@example.com'
    
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_verify_token_wrong_issuer(self, mock_verify: Any) -> None:
        mock_verify.return_value = {
            'iss': 'evil.com',
            'sub': '12345',
            'email': 'test@example.com'
        }
        
        result = GoogleLoginService.verify_google_token('invalid_token')
        
        assert result is None
    
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_verify_token_value_error(self, mock_verify: Any) -> None:
        mock_verify.side_effect = ValueError("Invalid token")
        
        result = GoogleLoginService.verify_google_token('invalid_token')
        
        assert result is None
    
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_google_verify_token_general_exception(self, mock_verify: Any) -> None:
        mock_verify.side_effect = Exception("Network error")
        
        result = GoogleLoginService.verify_google_token('invalid_token')
        
        assert result is None
    
    @pytest.mark.django_db
    def test_google_get_or_create_user_new_user(self) -> None:
        google_user_info = {
            'sub': '12345',
            'email': 'newuser@example.com',
            'name': 'TestGoogleUser',
            'picture': 'https://example.com/picture.jpg'
        }
        
        user = GoogleLoginService.get_or_create_user(google_user_info)
        
        assert user is not None
        assert user.google_id == '12345'
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'TestGoogleUser'
        assert user.profile_image == 'https://example.com/picture.jpg'
        assert user.personal_info_consent is False
        assert user.terms_of_use is False
    
    @pytest.mark.django_db
    def test_google_get_or_create_user_existing_by_google_id(self) -> None:
        # 기존 사용자 생성
        existing_user = User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123',
            google_id='12345',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        google_user_info = {
            'sub': '12345',
            'email': 'existing@example.com',
            'name': 'Existing User'
        }
        
        user = GoogleLoginService.get_or_create_user(google_user_info)
        
        assert user is not None
        assert user.id == existing_user.id
        assert user.google_id == '12345'
    
    @pytest.mark.django_db
    def test_google_get_or_create_user_existing_by_email(self) -> None:
        # 기존 사용자 생성 (Google ID 없음)
        existing_user = User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        google_user_info = {
            'sub': '12345',
            'email': 'existing@example.com',
            'name': 'Existing User'
        }
        
        user = GoogleLoginService.get_or_create_user(google_user_info)
        
        assert user is not None
        assert user.id == existing_user.id
        assert user.google_id == '12345'
    
    @pytest.mark.django_db
    def test_google_get_or_create_user_missing_data(self) -> None:
        google_user_info = {
            'sub': '12345',
            'email': '',
            'name': 'Test User'
        }
        
        with pytest.raises(ValueError, match="Google 사용자 정보가 없습니다"):
            GoogleLoginService.get_or_create_user(google_user_info)
    
    @pytest.mark.django_db
    def test_google_authenticate_user_success(self) -> None:
        google_user_info = {
            'sub': '12345',
            'email': 'test@example.com',
            'name': 'Test User',
            'picture': 'https://example.com/picture.jpg'
        }
        
        with patch.object(GoogleLoginService, 'verify_google_token', return_value=google_user_info):
            user, error = GoogleLoginService.authenticate_user('valid_token')
            
            assert user is not None
            assert error is None
            assert user.google_id == '12345'
            assert user.email == 'test@example.com'
    
    @pytest.mark.django_db
    def test_google_authenticate_user_token_verification_failed(self) -> None:
        with patch.object(GoogleLoginService, 'verify_google_token', return_value=None):
            user, error = GoogleLoginService.authenticate_user('invalid_token')
            
            assert user is None
            assert error == "Google 토큰 검증에 실패했습니다."
    
    @pytest.mark.django_db
    def test_google_authenticate_user_creation_failed(self) -> None:
        google_user_info = {
            'sub': '12345',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        
        with patch.object(GoogleLoginService, 'verify_google_token', return_value=google_user_info), \
             patch.object(GoogleLoginService, 'get_or_create_user', return_value=None):
            user, error = GoogleLoginService.authenticate_user('valid_token')
            
            assert user is None
            assert error == "사용자 생성/조회에 실패했습니다."
    
    @pytest.mark.django_db
    def test_google_authenticate_user_exception(self) -> None:
        with patch.object(GoogleLoginService, 'verify_google_token', side_effect=Exception("Database error")):
            user, error = GoogleLoginService.authenticate_user('valid_token')
            
            assert user is None
            assert error == "Database error"
    
    @pytest.mark.django_db
    def test_kakao_generate_unique_username(self) -> None:
        # 기존 사용자가 없는 경우
        username = KakaoLoginService._generate_unique_username('카카오사용자')
        assert username == '카카오사용자'
        
        # 기존 사용자가 있는 경우
        User.objects.create_user(
            username='카카오사용자', 
            email='existing@example.com',
            personal_info_consent=True,
            terms_of_use=True
        )
        username = KakaoLoginService._generate_unique_username('카카오사용자')
        assert username == '카카오사용자_1'
    
    @pytest.mark.django_db
    @patch('requests.get')
    def test_kakao_get_user_info_success(self, mock_get: Any) -> None:
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 12345,
            'kakao_account': {
                'email': 'test@kakao.com',
                'profile': {
                    'nickname': '카카오사용자',
                    'profile_image_url': 'https://example.com/image.jpg'
                }
            }
        }
        mock_get.return_value = mock_response
        
        result = KakaoLoginService.get_kakao_user_info('valid_token')
        
        assert result is not None
        assert result['id'] == 12345
        assert result['kakao_account']['email'] == 'test@kakao.com'
    
    @pytest.mark.django_db
    @patch('requests.get')
    def test_kakao_get_user_info_failure(self, mock_get: Any) -> None:
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = 'Unauthorized'
        mock_get.return_value = mock_response
        
        result = KakaoLoginService.get_kakao_user_info('invalid_token')
        
        assert result is None
    
    @pytest.mark.django_db
    def test_kakao_get_or_create_user_new_user(self) -> None:
        kakao_user_info = {
            'id': 12345,
            'kakao_account': {
                'email': 'newuser@kakao.com',
                'profile': {
                    'nickname': '카카오사용자',
                    'profile_image_url': 'https://example.com/picture.jpg'
                }
            }
        }
        
        user = KakaoLoginService.get_or_create_user(kakao_user_info)
        
        assert user is not None
        assert user.kakao_id == '12345'
        assert user.email == 'newuser@kakao.com'
        assert user.first_name == '카카오사용자'
        assert user.profile_image == 'https://example.com/picture.jpg'
        assert user.personal_info_consent is False
        assert user.terms_of_use is False
    
    @pytest.mark.django_db
    def test_kakao_authenticate_user_success(self) -> None:
        kakao_user_info = {
            'id': 12345,
            'kakao_account': {
                'email': 'test@kakao.com',
                'profile': {
                    'nickname': '카카오사용자',
                    'profile_image_url': 'https://example.com/picture.jpg'
                }
            }
        }
        
        with patch.object(KakaoLoginService, 'get_kakao_user_info', return_value=kakao_user_info):
            user, error = KakaoLoginService.authenticate_user('valid_token')
            
            assert user is not None
            assert error is None
            assert user.kakao_id == '12345'
            assert user.email == 'test@kakao.com'