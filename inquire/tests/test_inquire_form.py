import pytest

from config.utils.setup_test_method import TestSetupMixin
from inquire.forms.inqurie_create import InquireForm


@pytest.mark.django_db
class TestInquireCreateForm(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()

    def test_inquire_form_authenticated_user(self) -> None:
        form = InquireForm(user=self.customer_user)

        assert 'email' not in form.fields
        assert 'title' in form.fields
        assert 'content' in form.fields
        assert 'item' in form.fields

    def test_inquire_form_anonymous_user(self) -> None:
        form = InquireForm(user=None)

        assert 'email' in form.fields
        email_field = form.fields['email']
        assert email_field.required is True
        assert email_field.label == '이메일'
        assert email_field.widget.attrs['placeholder'] == '답변받을 이메일 주소를 입력해주세요.'


    def test_inquire_form_validation(self) -> None:
        data = {
            'email': 'user@example.com',
            'title': '배송이 안와요',
            'content': '언제쯤 도착하나요?',
            'item': 'delivery'
        }
        form = InquireForm(data=data, user=None)

        assert form.is_valid()
