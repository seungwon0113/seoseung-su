import pytest

from config.utils.setup_test_method import TestSetupMixin
from products.templatetags.product_filters import discount_amount, discount_rate


@pytest.mark.django_db
class TestProductFilter(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()

    def test_discount_rate(self) -> None:
        assert discount_rate(10000, 8000) == 20
        assert discount_rate(10000, 0) == 0

    def test_discount_amount(self) -> None:
        assert discount_amount(10000, 8000) == 2000
        assert discount_amount(10000, 0) == 10000
        assert discount_amount(0, 8000) == 0