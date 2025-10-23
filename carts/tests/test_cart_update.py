import pytest

from carts.forms.update import CartUpdateForm  # 실제 경로에 맞게 조정
from config.utils.setup_test_method import TestSetupMixin


@pytest.mark.django_db
class TestCartUpdate(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()

    def test_form_valid_quantity(self) -> None:
        form = CartUpdateForm(data={'quantity': 3})
        assert form.is_valid()
        assert form.cleaned_data['quantity'] == 3

    def test_form_quantity_is_zero(self) -> None:
        form = CartUpdateForm(data={'quantity': 0})
        assert not form.is_valid()
        assert 'quantity' in form.errors
        assert form.errors['quantity'] == ['수량은 1개 이상이어야 합니다.']

    def test_form_quantity_is_negative(self) -> None:
        form = CartUpdateForm(data={'quantity': -5})
        assert not form.is_valid()
        assert 'quantity' in form.errors
        assert form.errors['quantity'] == ['수량은 1개 이상이어야 합니다.']