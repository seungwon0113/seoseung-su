import pytest

from config.utils.setup_test_method import TestSetupMixin
from reviews.forms.review_create import ReviewForm
from reviews.models import Review
from reviews.services.review_count import ReviewCountService


@pytest.mark.django_db
class TestReviewRatingCount(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()
        self.review_rating_field_name = Review._meta.get_field('rating').name


    def test_review_rating_average(self) -> None:
        stats = ReviewCountService.get_product_review_stats(self.product)
        assert stats['review_count'] == 2
        assert stats['avg_rating'] == 4.5

    def test_valid_rating(self) -> None:
        form = ReviewForm(data={'content':'Test Review Rating', 'rating': 5})
        assert form.is_valid()
        assert form.cleaned_data['rating'] == 5

    @pytest.mark.parametrize('invalid_rating', [0, -1, 6, 10])
    def test_invalid_rating(self, invalid_rating : int) -> None:
        form = ReviewForm(data={'content': 'Test Review', 'rating': invalid_rating})

        assert not form.is_valid()
        assert self.review_rating_field_name in form.errors
        error_msgs = "".join([str(err) for err in form.errors['rating']])
        assert (
                "평점은 1점부터 5점까지 선택 가능합니다." in error_msgs
                or "Ensure this value is greater than or equal to 0." in error_msgs
        )
    def test_empty_rating(self) -> None:
        form = ReviewForm(data={'content': '적절한 내용'})
        assert not form.is_valid()
        assert self.review_rating_field_name in form.errors