import json

import pytest
from django.urls import reverse

from config.utils.setup_test_method import TestSetupMixin
from reviews.models import ReviewComment


@pytest.mark.django_db
class TestReviewCommentCreate(TestSetupMixin):

    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()

    def test_update_review_comment_handle_permissions(self) -> None:
        self.client.force_login(user=self.customer_user)

        comment = ReviewComment.objects.create(
            review=self.customer_review,
            user=self.customer_user,
            content="일반 유저 댓글",
            is_published=True,
        )

        url = reverse("review-comment-update", kwargs={"comment_id": comment.id})
        data = {"content": "관리자 전용 수정", "is_published": False}
        response = self.client.generic(
            method="POST",
            path=url,
            data=json.dumps(data),
            content_type="application/json",
        )

        assert response.status_code == 403
        response_json = response.json()
        assert response_json["success"] is False
        assert response_json["error"] == "권한이 없습니다."


    def test_review_comment_update(self) -> None:
        self.client.force_login(user=self.admin_user)

        admin_comment = ReviewComment.objects.create(
            review=self.customer_review,
            user=self.admin_user,
            content='기존 답변 내용입니다.',
            is_published=True,
        )

        url = reverse('review-comment-update', kwargs={'comment_id': admin_comment.id})

        data = {
            "content": "수정된 관리자 댓글입니다.",
            "is_published": False,
        }

        response = self.client.generic(
            method="POST",
            path=url,
            data=json.dumps(data),
            content_type="application/json"
        )

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["success"] is True
        assert response_json["comment"]["content"] == "수정된 관리자 댓글입니다."

        admin_comment.refresh_from_db()
        assert admin_comment.content == "수정된 관리자 댓글입니다."
        assert not admin_comment.is_published


    def test_review_comment_update_invalid_json(self) -> None:
        self.client.force_login(user=self.admin_user)
        admin_comment = ReviewComment.objects.create(
            review=self.customer_review, user=self.admin_user, content="테스트", is_published=True
        )

        url = reverse('review-comment-update', kwargs={'comment_id': admin_comment.id})

        response = self.client.post(url, data="not json", content_type="application/json")
        assert response.status_code == 400
        assert response.json()["error"] == "잘못된 요청입니다."


    def test_review_comment_update_validation_error(self) -> None:
        self.client.force_login(user=self.admin_user)
        admin_comment = ReviewComment.objects.create(
            review=self.customer_review, user=self.admin_user, content="테스트", is_published=True
        )
        url = reverse('review-comment-update', kwargs={'comment_id': admin_comment.id})

        long_content = "a" * 501
        data = {"content": long_content, "is_published": True}
        response = self.client.generic(
            method="POST", path=url, data=json.dumps(data), content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert "content" in response.json()["errors"]