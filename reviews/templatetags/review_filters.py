from django import template

from reviews.models import Review
from reviews.services.review_count import ReviewCountService

register = template.Library()


@register.filter
def product_avg_rating(review: Review) -> float:
    return ReviewCountService.get_product_review_stats(review.product)['avg_rating']


@register.filter
def product_review_count(review: Review) -> float:
    return ReviewCountService.get_product_review_stats(review.product)['review_count']
