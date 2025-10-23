from django.db.models import Prefetch
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View

from products.models import Product
from reviews.forms.review_create import ReviewCommentForm, ReviewForm, ReviewImageForm
from reviews.models import Review, ReviewComment
from reviews.services.review_count import ReviewCountService


class ProductsDetailView(View):
    def get(self, request: HttpRequest, product_name: str) -> HttpResponse:
        products = get_object_or_404(Product, name=product_name)
        
        # 해당 제품의 리뷰 가져오기 (모든 댓글 포함 - 템플릿에서 권한에 따라 표시)
        reviews = Review.objects.filter(
            product=products,
            is_published=True
        ).select_related('user').prefetch_related(
            'images', 
            Prefetch('comments', queryset=ReviewComment.objects.all().select_related('user'))
        ).order_by('-created_at')
        
        # ReviewCountService를 사용하여 리뷰 통계 계산
        review_stats = ReviewCountService.get_product_review_stats(products)
        
        # 사용자가 이미 리뷰를 작성했는지 확인
        user_review = None
        if request.user.is_authenticated:
            user_review = next((review for review in reviews if review.user == request.user), None)
        
        # 리뷰 작성 폼
        review_form = ReviewForm()
        review_image_form = ReviewImageForm()
        
        # 댓글 폼
        comment_form = ReviewCommentForm()
        
        context = {
            "products": products,
            "reviews": reviews,
            "avg_rating": review_stats['avg_rating'],
            "review_count": review_stats['review_count'],
            "user_review": user_review,
            "review_form": review_form,
            "review_image_form": review_image_form,
            "comment_form": comment_form,
        }
        return render(request, "products/detail.html", context)