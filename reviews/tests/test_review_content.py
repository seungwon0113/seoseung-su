import pytest

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import ReviewComment


@pytest.mark.django_db
class TestReviewComment(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()
        self.review_content_field_name = ReviewComment

