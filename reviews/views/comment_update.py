import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from reviews.forms.review_create import ReviewCommentForm
from reviews.models import ReviewComment
from users.models import User


class ReviewCommentUpdateView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def post(self, request: HttpRequest, comment_id: int) -> HttpResponse:
        comment = get_object_or_404(ReviewComment, id=comment_id)

        # 관리자만 수정 가능
        if not request.user.is_authenticated or request.user.role != User.Role.ADMIN:
            return JsonResponse({
                'success': False,
                'error': '권한이 없습니다.'
            }, status=403)

        try:
            data = json.loads(request.body)
            form = ReviewCommentForm(data, instance=comment)

            if form.is_valid():
                updated_comment = form.save()
                
                return JsonResponse({
                    'success': True,
                    'comment': {
                        'id': updated_comment.id,
                        'content': updated_comment.content,
                        'is_published': updated_comment.is_published,
                        'created_at': updated_comment.created_at.strftime('%Y.%m.%d %H:%M')
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': '입력 내용을 확인해주세요.',
                    'errors': form.errors
                }, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': '잘못된 요청입니다.'
            }, status=400)
