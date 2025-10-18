import pytest

from config.utils.setup_test_method import TestSetupMixin


@pytest.mark.django_db
class TestReviewCreate(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()

    def test_create_review(self) -> None:
        self.client.force_login(user=self.customer_user)
        review = self.customer_review

        assert review.user == self.customer_user
        assert review.product == self.product
        assert review.content == 'Customer Review Content'
        assert review.rating == 4
        assert review.is_published is True
