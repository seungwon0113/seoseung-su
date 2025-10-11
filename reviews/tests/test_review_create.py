import pytest

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import Review


@pytest.mark.django_db
class TestReviewCreate(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_data()
    
    def test_create_review(self) -> None:
        self.client.force_login(user=self.user)
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            content='Test Review',
            rating=5
        )

        assert review.user == self.user
        assert review.product == self.product
        assert review.content == 'Test Review'
        assert review.rating == 5
        assert review.is_published is True
