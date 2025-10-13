import pytest

from config.utils.setup_test_method import TestSetupMixin
from products.forms.product_form import ProductForm


@pytest.mark.django_db
class TestSalePrice(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()

    def test_clean_sale_price_zero_or_less(self) -> None:
        form_data = {
            'price': 100.0,
            'sale_price': 0.0,
        }
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert 'sale_price' in form.errors
        assert form.errors['sale_price'] == ["할인가격은 0보다 커야 합니다."]

    def test_clean_sale_price_not_lower_than_price(self) -> None:
        form_data = {
            'price': 100.0,
            'sale_price': 150.0,
        }
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert 'sale_price' in form.errors
        assert form.errors['sale_price'] == ["할인가격은 정가보다 낮아야 합니다."]