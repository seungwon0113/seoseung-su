from typing import Any

from django import forms

from categories.models import Category


class CategoryForm(forms.ModelForm): # type: ignore
    class Meta:
        model = Category
        fields = ("name", "parent")
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # Parent 필드에는 대분류 카테고리들만 표시 (parent=None인 것들)
        parent_field = self.fields['parent']
        if hasattr(parent_field, 'queryset'):
            parent_field.queryset = Category.objects.filter(parent=None)
        if hasattr(parent_field, 'empty_label'):
            parent_field.empty_label = "대분류로 설정 (상위 카테고리 없음)"