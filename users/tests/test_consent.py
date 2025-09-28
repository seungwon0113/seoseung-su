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
        response = client.get(consent_url)
        
        assert response.status_code == 302
        assert '/users/login/' in response['Location']
    
    @pytest.mark.django_db
    def test_consent_view_already_consented_redirect(self, client: Client, consent_url: str, test_user_with_consent: 'User') -> None:
        client.force_login(test_user_with_consent)
        
        response = client.get(consent_url)
        
        assert response.status_code == 302
        assert response['Location'] == '/'
    
    @pytest.mark.django_db
    def test_consent_view_get_renders_template(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        client.force_login(test_user_without_consent)
        
        response = client.get(consent_url)
        
        assert response.status_code == 200
        assert 'users/consent.html' in [t.name for t in response.templates]
    
    @pytest.mark.django_db
    def test_consent_view_post_missing_required_consent(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        client.force_login(test_user_without_consent)
        
        response = client.post(consent_url, {
            'terms_of_use': '',
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
        client.force_login(test_user_without_consent)
        
        response = client.post(consent_url, {
            'terms_of_use': 'on',
            'personal_info_consent': 'on',
            'sns_consent_to_receive': 'on',
            'email_consent_to_receive': 'on'
        })
        
        assert response.status_code == 302
        assert response['Location'] == '/'
        
        test_user_without_consent.refresh_from_db()
        assert test_user_without_consent.terms_of_use is True
        assert test_user_without_consent.personal_info_consent is True
        assert test_user_without_consent.sns_consent_to_receive is True
        assert test_user_without_consent.email_consent_to_receive is True
    
    @pytest.mark.django_db
    def test_consent_view_post_partial_consent(self, client: Client, consent_url: str, test_user_without_consent: 'User') -> None:
        client.force_login(test_user_without_consent)
        
        response = client.post(consent_url, {
            'terms_of_use': 'on',
            'personal_info_consent': 'on',
        })
        
        assert response.status_code == 302
        assert response['Location'] == '/'
        
        test_user_without_consent.refresh_from_db()
        assert test_user_without_consent.terms_of_use is True
        assert test_user_without_consent.personal_info_consent is True
        assert test_user_without_consent.sns_consent_to_receive is False
        assert test_user_without_consent.email_consent_to_receive is False
