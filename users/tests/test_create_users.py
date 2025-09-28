from typing import Any

import pytest
from django.test import Client
from pytest import MonkeyPatch

from users.models import User


@pytest.mark.django_db
class TestSignupUsers:

    def setup_method(self) -> None:
        self.client = Client()


    def test_signup_get_redirect_authenticated(self) -> None:
        User.objects.create_user(username='signup', email='signup@signup.com', password='signup', phone_number='00000000000', personal_info_consent=True, terms_of_use=True)
        self.client.login(email='signup@signup.com', password='signup')
        response = self.client.get('/users/signup/')
        assert response.status_code == 302
        assert response.headers['Location'] == '/'
        assert len(response.templates) == 0

    def test_signup_get_renders_for_anonymous(self) -> None:
        response = self.client.get('/users/signup/')
        assert response.status_code == 200
        # 템플릿이 렌더되어 컨텐츠 일부가 포함되는지 확인
        content = response.content.decode()
        assert '회원가입' in content

    def test_signup_post_with_valid_form_redirects(self) -> None:
        response = self.client.post("/users/signup/", {
            "username": "signup",
            "email": "signup@signup.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "00000000000",
            "personal_info_consent": "on",
            "terms_of_use": "on",
            "sns_consent_to_receive": "on",
            "email_consent_to_receive": "on"
        })
        assert response.status_code == 302
        assert response.headers["Location"] == "/users/login/"

    def test_signup_post_service_error_renders_form_error(self, monkeypatch: MonkeyPatch) -> None:
        # 서비스에서 ValueError가 발생하는 경우 (예: DB 무결성 위반을 서비스가 래핑)
        from users.services import user_signup as service_module
        def raise_value_error(*args: Any, **kwargs: Any) -> None:
            raise ValueError("이미 존재하는 아이디 또는 이메일입니다.")
        monkeypatch.setattr(service_module.UserService, 'create_and_login_user', raise_value_error)

        response = self.client.post('/users/signup/', {
            "username": "serviceerr",
            "email": "serviceerr@example.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "01012121212",
            "personal_info_consent": "on",
            "terms_of_use": "on",
        })
        # 리다이렉트가 아닌 동일 페이지 렌더링
        assert response.status_code == 200
        assert '이미 존재하는 아이디 또는 이메일입니다.' in response.content.decode()

    def test_signup_post_invalid_form_shows_errors(self) -> None:
        response = self.client.post("/users/signup/", {
            "username": "",
            "email": "invalid-email",
            "password": "123",
            "passwordConfirm": "456",
            "phone_number": "",
            "personal_info_consent": "",  # 동의 안 함 → invalid
            "terms_of_use": "",  # 필수 동의 안 함
        })
        assert response.status_code == 200
        content = response.content.decode()
        assert "이름을 입력해 주세요." in content
        assert "비밀번호는 최소 6자 이상이어야 합니다." in content
        # assert "비밀번호가 일치하지 않습니다." in content

    def test_signup_post_duplicate_username_shows_error(self) -> None:
        User.objects.create_user(
            username='dupuser', email='dupuser@example.com', password='x',
            phone_number='01000000000', personal_info_consent=True, terms_of_use=True
        )
        response = self.client.post("/users/signup/", {
            "username": "dupuser",
            "email": "new@example.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "01012345678",
            "personal_info_consent": "on",
            "terms_of_use": "on",
        })
        assert response.status_code == 200
        assert "이미 존재하는 아이디입니다." in response.content.decode()

    def test_signup_post_duplicate_email_shows_error(self) -> None:
        User.objects.create_user(
            username='newuser', email='dup@example.com', password='x',
            phone_number='01099999999', personal_info_consent=True, terms_of_use=True
        )
        response = self.client.post("/users/signup/", {
            "username": "another",
            "email": "dup@example.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "01088888888",
            "personal_info_consent": "on",
            "terms_of_use": "on",
        })
        assert response.status_code == 200
        assert "이미 가입된 이메일입니다." in response.content.decode()

    def test_signup_post_duplicate_phone_number_shows_error(self) -> None:
        User.objects.create_user(
            username='p1', email='p1@example.com', password='x',
            phone_number='01077777777', personal_info_consent=True, terms_of_use=True
        )
        response = self.client.post("/users/signup/", {
            "username": "p2",
            "email": "p2@example.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone1": "010",
            "phone2": "7777",
            "phone3": "7777",
            "phone_number": "01077777777",
            "personal_info_consent": "on",
            "terms_of_use": "on",
        })
        assert response.status_code == 200
        assert "이미 등록된 휴대폰 번호입니다." in response.content.decode()

    def test_signup_post_with_optional_consent_works(self) -> None:
        """선택 동의 항목 없이도 회원가입이 가능한지 테스트"""
        response = self.client.post("/users/signup/", {
            "username": "optionaltest",
            "email": "optional@example.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "01055555555",
            "personal_info_consent": "on",
            "terms_of_use": "on",
        })
        assert response.status_code == 302
        assert response.headers["Location"] == "/users/login/"
        
        # 사용자가 생성되었는지 확인
        user = User.objects.get(username="optionaltest")
        assert not user.sns_consent_to_receive
        assert not user.email_consent_to_receive

    def test_signup_post_with_all_consent_works(self) -> None:
        """모든 동의 항목을 체크했을 때 회원가입이 가능한지 테스트"""
        response = self.client.post("/users/signup/", {
            "username": "allconsent",
            "email": "allconsent@example.com",
            "password": "signup",
            "passwordConfirm": "signup",
            "phone_number": "01066666666",
            "personal_info_consent": "on",
            "terms_of_use": "on",
            "privacy_consent": "on",
            "sns_consent_to_receive": "on",
            "email_consent_to_receive": "on"
        })
        assert response.status_code == 302
        assert response.headers["Location"] == "/users/login/"
        
        # 사용자가 생성되었는지 확인
        user = User.objects.get(username="allconsent")
        assert user.terms_of_use
        assert user.sns_consent_to_receive
        assert user.email_consent_to_receive

