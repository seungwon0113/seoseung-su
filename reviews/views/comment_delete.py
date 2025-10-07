from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from reviews.models import ReviewComment
from users.models import User


class ReviewCommentDeleteView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request: HttpRequest, comment_id: int) -> HttpResponse:
        comment = get_object_or_404(ReviewComment, id=comment_id)

        # 관리자만 삭제 가능
        if not request.user.is_authenticated or request.user.role != User.Role.ADMIN:
            raise Http404("권한이 없습니다.")

        product_name = comment.review.product.name
        comment.delete()

        return redirect('products-detail', product_name=product_name)