import pytest
from django.test import RequestFactory
from django.test.client import Client

from users.models import User
from users.utils.permission import AdminPermission


@pytest.mark.django_db
class TestPermission:
    def setup_method(self) -> None:
        self.client = Client()

    def test_admin_permission_func(self) -> None:
        rf = RequestFactory()
        user = User.objects.create_user(
            username='test_admin_func',
            email='test_func@test.com',
            password='testtest',
            phone_number='00000000000',
            personal_info_consent=True,
            terms_of_use=True,
            role='admin'
        )
        request = rf.get('/fake-url/')
        request.user = user

        permission = AdminPermission()
        permission.request = request
        assert permission.test_func()