import pytest
from django.db.models import Avg

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import Review


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
        avg_rating_for_product = Review.objects.filter(product=self.product).aggregate(avg=Avg('rating'))['avg']
        assert avg_rating_for_product == 4.5




