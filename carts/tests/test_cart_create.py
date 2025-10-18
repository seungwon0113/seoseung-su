import pytest

from carts.models import Cart
from config.utils.setup_test_method import TestSetupMixin


@pytest.mark.django_db
class TestCartCreate(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()

    def test_products_added_customer_cart(self) -> None:
        self.client.force_login(self.customer_user)

        added_cart = Cart.objects.create(user=self.customer_user, product=self.product, quantity=2)
        assert added_cart.quantity == 2
        assert added_cart.product == self.product