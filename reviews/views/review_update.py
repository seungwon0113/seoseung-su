from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from reviews.forms.review_create import ReviewForm, ReviewImageForm
from reviews.models import Review, ReviewImage


class ReviewUpdateView(LoginRequiredMixin, View):
    login_url = '/users/login/'

    def get(self, request: HttpRequest, review_id: int) -> HttpResponse:
        review = get_object_or_404(Review, id=review_id)

        # 본인의 리뷰인지 확인
        if review.user != request.user:
            raise Http404("권한이 없습니다.")

        form = ReviewForm(instance=review)
        image_form = ReviewImageForm()

        context = {
            'form': form,
            'image_form': image_form,
            'review': review,
            'product': review.product
        }
        return render(request, 'reviews/review_update.html', context)

    def post(self, request: HttpRequest, review_id: int) -> HttpResponse:
        review = get_object_or_404(Review, id=review_id)

        # 본인의 리뷰인지 확인
        if review.user != request.user:
            raise Http404("권한이 없습니다.")

        form = ReviewForm(request.POST, instance=review)
        image_form = ReviewImageForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            form.save()

            # 새 이미지 추가
            images = request.FILES.getlist('image')
            if images:
                for image in images:
                    review_image = ReviewImage.objects.create(image=image)
                    review.images.add(review_image)

            return redirect('products-detail', product_name=review.product.name)

        context = {
            'form': form,
            'image_form': image_form,
            'review': review,
            'product': review.product
        }
        return render(request, 'reviews/review_update.html', context)