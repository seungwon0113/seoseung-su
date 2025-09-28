
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from products.models import ProductImage
from users.utils.permission import AdminPermission


class DeleteProductImageView(AdminPermission, View):
    def delete(self, request: HttpRequest, image_id: int) -> JsonResponse:
        try:
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()
            return JsonResponse({'success': True, 'message': '이미지가 삭제되었습니다.'})
        except Http404:
            return JsonResponse({'success': False, 'message': '이미지를 찾을 수 없습니다.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'삭제 중 오류가 발생했습니다: {str(e)}'}, status=500)


