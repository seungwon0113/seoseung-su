from typing import Any

import pytest
from django.db import IntegrityError
from django.test import RequestFactory
from pytest import MonkeyPatch

from users.services.user_signup import UserService


@pytest.mark.django_db
class TestUserService:

    def setup_method(self) -> None:
        self.rf = RequestFactory()

    def test_create_and_login_user_success(self, monkeypatch: MonkeyPatch) -> None:
        request = self.rf.post('/users/signup/')

        class DummyUser:
            def __init__(self) -> None:
                self.id = 1
                self.email = 'ok@example.com'

        def fake_create_user(**kwargs: Any) -> DummyUser:
            return DummyUser()

        # monkeypatch User.objects.create_user
        from users import models as user_models
        monkeypatch.setattr(user_models.User.objects, 'create_user', fake_create_user)

        user = UserService.create_and_login_user(request, {
            'username': 'ok',
            'email': 'ok@example.com',
            'password': 'secret',
            'personal_info_consent': True,
            'phone_number': '01011112222',
            'terms_of_use': True,
            'sns_consent_to_receive': True,
            'email_consent_to_receive': True
        })
        assert getattr(request, 'user', None) is user

    def test_create_and_login_user_integrity_error_raises_value_error(self, monkeypatch: MonkeyPatch) -> None:
        request = self.rf.post('/users/signup/')

        def raise_integrity_error(**kwargs: Any) -> None:
            raise IntegrityError()

        from users import models as user_models
        monkeypatch.setattr(user_models.User.objects, 'create_user', raise_integrity_error)

        with pytest.raises(ValueError) as exc:
            UserService.create_and_login_user(request, {
                'username': 'dup',
                'email': 'dup@example.com',
                'password': 'secret',
                'personal_info_consent': True,
                'phone_number': '01033334444',
                'terms_of_use': True,
            })
        assert '이미 존재하는 아이디 또는 이메일입니다.' in str(exc.value)


