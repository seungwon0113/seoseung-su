import pytest
from django.contrib.auth.models import AnonymousUser

from config.utils.setup_test_method import TestSetupMixin
from inquire.services.inquire_user_valid import InquireUserValidService


@pytest.mark.django_db
class TestInquireUserValid(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()

    def test_inquire_user_valid_authenticated(self) -> None:
        self.client.force_login(self.customer_user)

        user, user_email = InquireUserValidService.validate_inquire_user_valid(self.customer_user)

        assert user == self.customer_user
        assert  user_email == self.customer_user.email

    def test_inquire_user_valid_anonymous(self) -> None:
        user = AnonymousUser()

        anon_user, anon_email = InquireUserValidService.validate_inquire_user_valid(user)

        assert anon_user is None
        assert anon_email is None

    def test_inquire_create(self) -> None:
        inquire = InquireUserValidService.create_inquire(
            user=self.customer_user,
            email=self.customer_user.email,
            title="배송이 안 와요",
            content="언제쯤 배송되는지 확인 부탁드려요",
            item="delivery"
        )

        assert inquire.id is not None
        assert inquire.user == self.customer_user
        assert inquire.email == "customer@customer.com"
        assert inquire.title == "배송이 안 와요"
        assert inquire.item == "delivery"
