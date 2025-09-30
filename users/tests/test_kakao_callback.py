from typing import TYPE_CHECKING, Any
from unittest.mock import Mock, patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

if TYPE_CHECKING:
    from users.models import User

User = get_user_model()  # type: ignore

@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def kakao_callback_url() -> str:
    return reverse('kakao-callback')


@pytest.fixture
def test_user() -> 'User':
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        personal_info_consent=True,
        terms_of_use=True
    )


class TestKakaoCallbackView:
    
    def test_kakao_callback_missing_code(self, client: Client, kakao_callback_url: str) -> None:
        response = client.get(kakao_callback_url)
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '인증 코드가 없습니다.'
    
    @patch('requests.post')
    def test_kakao_callback_token_request_failure(self, mock_post: Any, client: Client, kakao_callback_url: str) -> None:
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        response = client.get(f"{kakao_callback_url}?code=test_code")
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '액세스 토큰 획득에 실패했습니다.'
    
    @patch('requests.post')
    def test_kakao_callback_missing_access_token(self, mock_post: Any, client: Client, kakao_callback_url: str) -> None:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # access_token이 없음
        mock_post.return_value = mock_response
        
        response = client.get(f"{kakao_callback_url}?code=test_code")
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '액세스 토큰이 없습니다.'
    
    @pytest.mark.django_db
    @patch('requests.post')
    @patch('users.services.social_login.KakaoLoginService.authenticate_user')
    def test_kakao_callback_authentication_failure(self, mock_authenticate: Any, mock_post: Any, client: Client, kakao_callback_url: str) -> None:
        # 토큰 요청 성공 모킹
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response
        
        # 인증 실패 모킹
        mock_authenticate.return_value = (None, "인증 실패")
        
        response = client.get(f"{kakao_callback_url}?code=test_code")
        
        assert response.status_code == 400
        data = response.json()
        assert not data['success']
        assert data['message'] == '인증 실패'
    
    @pytest.mark.django_db
    @patch('requests.post')
    @patch('users.services.social_login.KakaoLoginService.authenticate_user')
    def test_kakao_callback_success_with_consent_redirect(self, mock_authenticate: Any, mock_post: Any, client: Client, kakao_callback_url: str) -> None:
        # 동의가 완료되지 않은 사용자 생성
        user = User.objects.create_user(
            username='kakaouser',
            email='kakao@example.com',
            personal_info_consent=False,  # 동의 미완료
            terms_of_use=False  # 동의 미완료
        )
        
        # 토큰 요청 성공 모킹
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response
        
        # 인증 성공 모킹
        mock_authenticate.return_value = (user, None)
        
        response = client.get(f"{kakao_callback_url}?code=test_code")
        
        assert response.status_code == 302
        assert response['Location'] == '/'
    
    @pytest.mark.django_db
    @patch('requests.post')
    @patch('users.services.social_login.KakaoLoginService.authenticate_user')
    def test_kakao_callback_success_with_home_redirect(self, mock_authenticate: Any, mock_post: Any, client: Client, kakao_callback_url: str, test_user: 'User') -> None:
        # 토큰 요청 성공 모킹
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response
        
        # 인증 성공 모킹 (동의 완료된 사용자)
        mock_authenticate.return_value = (test_user, None)
        
        response = client.get(f"{kakao_callback_url}?code=test_code")
        
        assert response.status_code == 302
        assert response['Location'] == '/'
    
    @patch('requests.post')
    @patch('users.services.social_login.KakaoLoginService.authenticate_user')
    def test_kakao_callback_server_error(self, mock_authenticate: Any, mock_post: Any, client: Client, kakao_callback_url: str) -> None:
        # 토큰 요청에서 예외 발생
        mock_post.side_effect = Exception("Network error")
        
        response = client.get(f"{kakao_callback_url}?code=test_code")
        
        assert response.status_code == 500
        data = response.json()
        assert not data['success']
        assert '서버 오류가 발생했습니다' in data['message']
