import pytest
from django.urls import reverse

from config.utils.setup_test_method import TestSetupMixin
from reviews.forms.review_create import ReviewCommentForm
from reviews.models import ReviewComment


@pytest.mark.django_db
class TestReviewCommentCreate(TestSetupMixin):

    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()
        self.review_comment_field_name = ReviewComment._meta.get_field('content').name
    
    def test_create_review_comment(self) -> None:
        self.client.force_login(user=self.admin_user)
        comment = ReviewComment.objects.create(
            review=self.customer_review,
            user=self.admin_user,
            content='Great review!'
        )

        assert comment.review == self.customer_review
        assert comment.user == self.admin_user
        assert comment.content == 'Great review!'
        assert comment.is_published is True
    
    def test_review_comment_relationship(self) -> None:
        comment = ReviewComment.objects.create(
            review=self.customer_review,
            user=self.admin_user,
            content='Nice product!'
        )
        
        comments = self.customer_review.comments.all()
        assert comment in comments
        assert comments.count() == 1

    def test_valid_content(self) -> None:
        form = ReviewCommentForm(data={'content': '정상 입력', 'is_published': True})
        assert form.is_valid()
        assert form.cleaned_data['content'] == '정상 입력'

    def test_review_comment_create(self) -> None:
        self.client.force_login(user=self.admin_user)

        url = reverse('review-comment-create', kwargs={'review_id': self.customer_review.id})
        data = {
            'content': '특정 리뷰에 대한 관리자의 답변',
            'is_published': True,
        }

        response = self.client.post(url, data)
        assert response.status_code == 302
        assert ReviewComment.objects.filter(content='특정 리뷰에 대한 관리자의 답변').exists()