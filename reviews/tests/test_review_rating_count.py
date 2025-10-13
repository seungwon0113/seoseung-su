import pytest

from config.utils.setup_test_method import TestSetupMixin
from reviews.services.review_count import ReviewCountService


@pytest.mark.django_db
class TestReviewRatingCount(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()


    def test_review_rating_average(self) -> None:
        stats = ReviewCountService.get_product_review_stats(self.product)
        assert stats['review_count'] == 2
        assert stats['avg_rating'] == 4.5




