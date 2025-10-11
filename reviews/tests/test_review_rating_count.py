import pytest

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import Review
from reviews.services.review_count import ReviewCountService


@pytest.mark.django_db
class TestReviewRatingCount(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_data()
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            content='Customer Review Content',
            rating=4
        )
        self.admin_review = Review.objects.create(
            product=self.product,
            user=self.admin_user,
            content='Admin Review Content',
            rating=5
        )

    def test_review_rating_average(self) -> None:
        # 특정 상품에 대한 평점 평균
        stats = ReviewCountService.get_product_review_stats(self.product)
        assert stats['review_count'] == 2
        assert stats['avg_rating'] == 4.5




