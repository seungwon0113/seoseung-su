from django.urls import path

from reviews.views.comment_create import ReviewCommentCreateView
from reviews.views.comment_delete import ReviewCommentDeleteView
from reviews.views.image_delete import DeleteReviewImageView
from reviews.views.review_create import ReviewCreateView
from reviews.views.review_delete import ReviewDeleteView
from reviews.views.review_update import ReviewUpdateView

urlpatterns = [
    # 리뷰 CRUD
    path('create/<int:product_id>/', ReviewCreateView.as_view(), name='review-create'),
    path('update/<int:review_id>/', ReviewUpdateView.as_view(), name='review-update'),
    path('delete/<int:review_id>/', ReviewDeleteView.as_view(), name='review-delete'),
    path('image/delete/<int:image_id>/', DeleteReviewImageView.as_view(), name='review-image-delete'),
    path('comment/create/<int:review_id>/', ReviewCommentCreateView.as_view(), name='review-comment-create'),
    path('comment/delete/<int:comment_id>/', ReviewCommentDeleteView.as_view(), name='review-comment-delete'),
]

