import pytest
from django.test import Client

from categories.models import Category
from users.models import User


@pytest.mark.django_db
class TestCategories:
    def setup_method(self) -> None:
        self.client = Client()
        # 비밀번호를 제대로 해시하여 사용자 생성
        self.admin_user = User.objects.create_user(
            role="admin",  # admin으로 수정
            email="admin@admin.com", 
            password="create_test_admin", 
            username="create_test_user", 
            personal_info_consent=True, 
            terms_of_use=True
        )

    def test_create_category(self) -> None:
        user = self.admin_user
        assert user.role == "admin"
        if user.role == "admin":
            category = Category.objects.create(name="대분류카테고리", parent=None)
            
            assert category.id is not None
            assert category.name == "대분류카테고리"
            assert category.parent is None
            
            saved_category = Category.objects.get(name="대분류카테고리")
            assert saved_category.name == "대분류카테고리"

    def test_create_parent_category(self) -> None:
        user = User.objects.get(username="create_test_user")
        if user.role == "admin":
            category = Category.objects.create(name="대분류카테고리", parent=None)
            parent_category = Category.objects.create(name="소분류카테고리", parent=category)

            assert parent_category.id is not None
            assert parent_category.name == "소분류카테고리"
            assert parent_category.parent == category

            saved_parent_category = Category.objects.get(name="소분류카테고리")
            assert saved_parent_category.name == "소분류카테고리"

