from typing import TYPE_CHECKING

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
def consent_url() -> str:
    return reverse('consent')


@pytest.fixture
def test_user_with_consent() -> 'User':
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        personal_info_consent=True,
        terms_of_use=True
    )


@pytest.fixture
def test_user_without_consent() -> 'User':
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123',
        personal_info_consent=False,
        terms_of_use=False
    )


class TestConsentView:
    
    def test_consent_view_anonymous_redirect(self, client: Client, consent_url: str) -> None:
        """비로그인 사용자는 로그인 페이지로 리다이렉트"""
        response = client.get(consent_url)
        
        assert response.status_code == 302
        assert '/users/login/' in response['Location']
    
    @pytest.mark.django_db
    def test_consent_view_already_consented_redirect(self, client: Client, consent_url: str, test_user_with_consent: 'User') -> None:
        """이미 동의한 사용자는 홈페이지로 리다이렉트"""
        client.force_login(test_user_with_consent)
        
        response = client.get(consent_url)
        
        assert response.status_code == 302
        assert response['Location'] == '/'
    
    @pytest.mark.django_db
    def test_consent_view_get_renders_template(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        """동의가 필요한 사용자에게 동의 페이지 표시"""
        client.force_login(test_user_without_consent)
        
        response = client.get(consent_url)
        
        assert response.status_code == 200
        assert 'users/consent.html' in [t.name for t in response.templates]
    
    @pytest.mark.django_db
    def test_consent_view_post_missing_required_consent(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        """필수 동의 항목이 누락된 경우"""
        client.force_login(test_user_without_consent)
        
        response = client.post(consent_url, {
            'terms_of_use': '',  # 필수 동의 누락
            'personal_info_consent': 'on',
            'sns_consent_to_receive': 'on',
            'email_consent_to_receive': 'on'
        })
        
        assert response.status_code == 200
        messages = list(response.context['messages'])
        assert len(messages) > 0
        assert '필수 동의 항목에 모두 동의해주세요.' in str(messages[0])
    
    @pytest.mark.django_db
    def test_consent_view_post_success(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        """모든 필수 동의 항목 완료 시 성공"""
        client.force_login(test_user_without_consent)
        
        response = client.post(consent_url, {
            'terms_of_use': 'on',
            'personal_info_consent': 'on',
            'sns_consent_to_receive': 'on',
            'email_consent_to_receive': 'on'
        })
        
        assert response.status_code == 302
        assert response['Location'] == '/'
        
        # 사용자 동의 정보가 업데이트되었는지 확인
        test_user_without_consent.refresh_from_db()
        assert test_user_without_consent.terms_of_use is True
        assert test_user_without_consent.personal_info_consent is True
        assert test_user_without_consent.sns_consent_to_receive is True
        assert test_user_without_consent.email_consent_to_receive is True
    
    @pytest.mark.django_db
    def test_consent_view_post_partial_consent(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        """필수 동의만 하고 선택 동의는 안 한 경우"""
        client.force_login(test_user_without_consent)
        
        response = client.post(consent_url, {
            'terms_of_use': 'on',
            'personal_info_consent': 'on',
            # 선택 동의 항목은 체크하지 않음
        })
        
        assert response.status_code == 302
        assert response['Location'] == '/'
        
        # 사용자 동의 정보 확인
        test_user_without_consent.refresh_from_db()
        assert test_user_without_consent.terms_of_use is True
        assert test_user_without_consent.personal_info_consent is True
        assert test_user_without_consent.sns_consent_to_receive is False
        assert test_user_without_consent.email_consent_to_receive is False
