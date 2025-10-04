from typing import Any, Dict

from django.http import HttpRequest

from categories.models import Category


def categories_context(request: HttpRequest) -> Dict[str, Any]:
    main_categories = Category.objects.filter(parent=None).prefetch_related('children')[:4]
    return {
        'main_categories': main_categories
    }
