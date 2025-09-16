
import pytest
from django.test import Client

from users.models import User


@pytest.mark.django_db
class TestLoginView:

    def setup_method(self) -> None:
        """각 테스트 메서드 실행 전에 호출되는 설정"""
        self.client = Client()

    def test_login_get_request_returns_correct_template(self) -> None:
        """GET 요청시 올바른 템플릿이 렌더링되는지 테스트"""
        response = self.client.get('/users/login/')  # 또는 reverse('login') 사용
        assert response.status_code == 200
        assert 'users/login.html' in [t.name for t in response.templates]

    def test_login_get_redirect_authenticated(self) -> None:
        User.objects.create_user(username='test', email='test@test.com', password='testtest')
        self.client.login(email='test@test.com', password='testtest')
        response = self.client.get('/users/login/')
        assert response.status_code == 302
        assert response.headers['Location'] == '/'  # 실제 'home' 경로에 따라
        assert len(response.templates) == 0

    def test_login_post_with_valid_form_redirects(self) -> None:
        User.objects.create_user(
            username="test",
            email="test@test.com",
            password="testtest"
        )
        response = self.client.post("/users/login/", {
            "email": "test@test.com",
            "password": "testtest",
        })
        assert response.status_code == 302
        assert response.headers["Location"] == "/users/login/"

    def test_login_post_with_invalid_form_shows_errors(self) -> None:
        """유효하지 않은 폼 데이터로 POST 요청시 에러 표시 테스트"""
        User.objects.create_user(
            username="test",
            email="test@test.com",
            password="testtest"
        )
        response = self.client.post("/users/login/", {
            "email": "test@test.com",
            "password": "wrongpass",
        })
        assert response.status_code == 200
        assert "유효하지 않은 사용자명 또는 비밀번호입니다." in response.content.decode()