from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from categories.forms.category import CategoryForm
from categories.models import Category
from users.utils.permission import AdminPermission


class CategoryListView(AdminPermission, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = CategoryForm()
        # 모든 대분류 카테고리들과 그 하위 카테고리들 조회
        main_categories = Category.objects.filter(parent=None).prefetch_related('children')
        context = {
            'form': form,
            'main_categories': main_categories,
        }
        return render(request, "category/list_category.html", context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        """카테고리 생성 처리"""
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # 생성 후 다시 목록 페이지로 리다이렉트
            return self.get(request)
        
        # 폼이 유효하지 않으면 에러와 함께 다시 렌더링
        main_category = Category.objects.filter(parent=None).first()
        sub_categories = main_category.children.all() if main_category else []
        
        context = {
            'form': form,
            'category': main_category,
            'parent_category': sub_categories,
        }
        return render(request, "category/list_category.html", context)