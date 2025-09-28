import pytest
from django.test import Client

from users.models import User


@pytest.mark.django_db
class TestCheckDuplicateView:

    def setup_method(self) -> None:
        self.client = Client()

    def test_check_username_available(self) -> None:
        """사용 가능한 아이디 체크 테스트"""
        response = self.client.get('/users/check-duplicate/', {'username': 'available_user'})
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is True
        assert data['username']['message'] == '사용 가능한 아이디입니다.'
        assert data['email']['available'] is True
        assert data['email']['message'] == ''

    def test_check_username_duplicate(self) -> None:
        User.objects.create_user(
            username='duplicate_user',
            email='test@example.com',
            password='testpass',
            phone_number='01012345678',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        response = self.client.get('/users/check-duplicate/', {'username': 'duplicate_user'})
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is False
        assert data['username']['message'] == '이미 존재하는 아이디입니다.'
        assert data['email']['available'] is True
        assert data['email']['message'] == ''

    def test_check_email_available(self) -> None:
        response = self.client.get('/users/check-duplicate/', {'email': 'available@example.com'})
        assert response.status_code == 200
        
        data = response.json()
        assert data['email']['available'] is True
        assert data['email']['message'] == '사용 가능한 이메일입니다.'
        assert data['username']['available'] is True
        assert data['username']['message'] == ''

    def test_check_email_duplicate(self) -> None:
        User.objects.create_user(
            username='testuser',
            email='duplicate@example.com',
            password='testpass',
            phone_number='01012345678',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        response = self.client.get('/users/check-duplicate/', {'email': 'duplicate@example.com'})
        assert response.status_code == 200
        
        data = response.json()
        assert data['email']['available'] is False
        assert data['email']['message'] == '이미 가입된 이메일입니다.'
        assert data['username']['available'] is True
        assert data['username']['message'] == ''

    def test_check_both_username_and_email(self) -> None:
        # 기존 사용자 생성
        User.objects.create_user(
            username='existing_user',
            email='existing@example.com',
            password='testpass',
            phone_number='01012345678',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        response = self.client.get('/users/check-duplicate/', {
            'username': 'existing_user',
            'email': 'existing@example.com'
        })
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is False
        assert data['username']['message'] == '이미 존재하는 아이디입니다.'
        assert data['email']['available'] is False
        assert data['email']['message'] == '이미 가입된 이메일입니다.'

    def test_check_mixed_available_and_duplicate(self) -> None:
        # 기존 사용자 생성
        User.objects.create_user(
            username='existing_user',
            email='existing@example.com',
            password='testpass',
            phone_number='01012345678',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        response = self.client.get('/users/check-duplicate/', {
            'username': 'existing_user',  # 중복
            'email': 'new@example.com'    # 사용 가능
        })
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is False
        assert data['username']['message'] == '이미 존재하는 아이디입니다.'
        assert data['email']['available'] is True
        assert data['email']['message'] == '사용 가능한 이메일입니다.'

    def test_check_empty_parameters(self) -> None:
        response = self.client.get('/users/check-duplicate/')
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is True
        assert data['username']['message'] == ''
        assert data['email']['available'] is True
        assert data['email']['message'] == ''

    def test_check_whitespace_parameters(self) -> None:
        response = self.client.get('/users/check-duplicate/', {
            'username': '   ',
            'email': '   '
        })
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is True
        assert data['username']['message'] == ''
        assert data['email']['available'] is True
        assert data['email']['message'] == ''

    def test_check_username_case_sensitivity(self) -> None:
        # 기존 사용자 생성 (소문자)
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass',
            phone_number='01012345678',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        # 대문자로 체크
        response = self.client.get('/users/check-duplicate/', {
            'username': 'TESTUSER'
        })
        assert response.status_code == 200
        
        data = response.json()
        # Django의 기본 User 모델은 username이 대소문자를 구분하므로 사용 가능해야 함
        assert data['username']['available'] is True
        assert data['username']['message'] == '사용 가능한 아이디입니다.'

    def test_check_special_characters(self) -> None:
        response = self.client.get('/users/check-duplicate/', {
            'username': 'user@123',
            'email': 'user+test@example.com'
        })
        assert response.status_code == 200
        
        data = response.json()
        assert data['username']['available'] is True
        assert data['username']['message'] == '사용 가능한 아이디입니다.'
        assert data['email']['available'] is True
        assert data['email']['message'] == '사용 가능한 이메일입니다.'
