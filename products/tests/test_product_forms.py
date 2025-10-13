import pytest

from config.utils.setup_test_method import TestSetupMixin
from products.forms.product_form import ProductForm


@pytest.mark.django_db
class TestProductForm(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()

    def test_product_form_invalid_price_negative(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': -100,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert 'price' in form.errors

    def test_product_form_invalid_price_zero(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 0,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert 'price' in form.errors

    def test_product_form_invalid_stock_negative(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000,
            'stock': -10,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert 'stock' in form.errors

    def test_product_form_missing_required_fields(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'price': 10000,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        assert not form.is_valid()
        assert 'description' in form.errors

    def test_product_form_clean_price_method(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000.50,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        form.is_valid()

    def test_product_form_clean_stock_method(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000,
            'stock': 50,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        form.is_valid()




