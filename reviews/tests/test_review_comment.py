import pytest

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import Review, ReviewComment


@pytest.mark.django_db
class TestReviewComment(TestSetupMixin):

    def setup_method(self) -> None:
        self.setup_test_data()
        
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            content='Test Review Content',
            rating=4
        )
    
    def test_create_review_comment(self) -> None:
        self.client.force_login(user=self.admin_user)
        comment = ReviewComment.objects.create(
            review=self.review,
            user=self.admin_user,
            content='Great review!'
        )

        assert comment.review == self.review
        assert comment.user == self.admin_user
        assert comment.content == 'Great review!'
        assert comment.is_published is True
    
    def test_review_comment_relationship(self) -> None:
        comment = ReviewComment.objects.create(
            review=self.review,
            user=self.admin_user,
            content='Nice product!'
        )
        
        comments = self.review.comments.all()
        assert comment in comments
        assert comments.count() == 1
