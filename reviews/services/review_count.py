from typing import Dict, Union

from django.db.models import Avg, Count

from products.models import Product
from reviews.models import Review


class ReviewCountService:
    @staticmethod
    def get_product_review_stats(product: Product) -> Dict[str, Union[float, int]]:
        reviews = Review.objects.filter(product=product)
        
        stats = reviews.aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        
        return {
            'avg_rating': float(stats['avg_rating']) if stats['avg_rating'] is not None else 0.0,
            'review_count': stats['review_count']
        }