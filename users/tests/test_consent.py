import pytest
from django.test import Client
from django.urls import reverse


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def consent_url() -> str:
    return reverse('personal_info_consent')

@pytest.mark.django_db
class TestPersonalInfoConsentView:
    """
    PersonalInfoConsent 뷰는 단순히 약관 내용을 보여주는 정적 페이지입니다.
    로그인 여부와 관계없이 누구나 접근할 수 있습니다.
    """
    
    def test_personal_info_consent_view_get_anonymous(self, client: Client, consent_url: str) -> None:
        """익명 사용자도 약관 페이지에 접근할 수 있어야 합니다."""
        response = client.get(consent_url)
        
        assert response.status_code == 200
        assert 'users/personal_info_consent.html' in [t.name for t in response.templates]
    
    def test_personal_info_consent_view_contains_terms_content(self, client: Client, consent_url: str) -> None:
        """약관 페이지에 필수 약관 내용이 포함되어 있어야 합니다."""
        response = client.get(consent_url)
        
        assert response.status_code == 200
        content = response.content.decode('utf-8')
        
        # 주요 약관 내용이 포함되어 있는지 확인
        assert '쇼핑몰 개인정보 처리방침' in content
        assert '제1조(목적)' in content
        assert '제17조(개인정보보호)' in content
        assert '카카오톡 알림톡 시행에 관한 내용' in content
        assert '제 N 조(포인트 및 쿠폰)' in content

    def test_personal_info_consent_view_post_not_allowed(self, client: Client, consent_url: str) -> None:
        response = client.post(consent_url, {})

        # POST 메서드는 허용되지 않으므로 405 Method Not Allowed 응답
        assert response.status_code == 405
