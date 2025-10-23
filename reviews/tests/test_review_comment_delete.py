import pytest
from django.urls import reverse

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import ReviewComment


@pytest.mark.django_db
class TestReviewCommentDelete(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()

        self.admin_review_comment = ReviewComment.objects.create(
            review=self.customer_review,
            user=self.admin_user,
            content="특정 리뷰에 대한 관리자의 답글",
            is_published=True,
        )

    def test_review_comment_delete(self) -> None:
        self.client.force_login(self.admin_user)

        url = reverse('review-comment-delete', kwargs={'comment_id': self.admin_review_comment.id})
        response = self.client.post(url, follow=True)
        assert response.status_code == 200
        assert not ReviewComment.objects.filter(id=self.admin_review_comment.id).exists()

