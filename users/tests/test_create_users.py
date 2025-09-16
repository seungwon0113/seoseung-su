import pytest
from django.test import Client

from users.models import User


@pytest.mark.django_db
class TestSignupUsers:

    def setup_method(self) -> None:
        self.client = Client()


    def test_signup_get_redirect_authenticated(self) -> None:
        User.objects.create_user(username='signup', email='signup@signup.com', password='signup', phone_number='00000000000', personal_info_consent=True)
        self.client.login(email='signup@signup.com', password='signup')
        response = self.client.get('/users/signup/')
        assert response.status_code == 302
        assert response.headers['Location'] == '/'
        assert len(response.templates) == 0

    def test_signup_post_with_valid_form_redirects(self) -> None:
        response = self.client.post("/users/signup/", {
            "username": "signup",
            "email": "signup@signup.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "00000000000",
            "personal_info_consent": "on"
        })
        assert response.status_code == 302
        assert response.headers["Location"] == "/users/login/"

    def test_signup_user(self) -> None:
        User.objects.create_user(username='signup', email='signup@signup.com', password='signup', phone_number='00000000000', personal_info_consent=True)
        # DB에서 사용자 쿼리
        user = User.objects.get(email='signup@signup.com')
        assert user.username == 'signup'
        assert user.email == 'signup@signup.com'
        # 비밀번호 해시 검증
        assert user.check_password('signup')

    def test_signup_post_invalid_form_shows_errors(self) -> None:
        response = self.client.post("/users/signup/", {
            "username": "",
            "email": "invalid-email",
            "password": "123",
            "passwordConfirm": "456",
            "phone_number": "",
            "personal_info_consent": "",  # 동의 안 함 → invalid
        })
        assert response.status_code == 200
        content = response.content.decode()
        assert "이름을 입력해 주세요." in content
        assert "비밀번호는 최소 6자 이상이어야 합니다." in content
        assert "비밀번호가 일치하지 않습니다." in content

