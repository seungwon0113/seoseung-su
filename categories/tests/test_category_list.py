import pytest
from django.urls import reverse

from categories.models import Category
from config.utils.setup_test_method import TestSetupMixin


@pytest.mark.django_db
class TestCategoryList(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_data()
        self.category = Category.objects.create(name="대분류", parent=None)
        self.parent_category = Category.objects.create(name="소분류", parent=self.category)

    def test_category_list(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse("category-list")
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context

        main_categories = response.context["main_categories"]
        assert self.category in main_categories
        assert self.parent_category in self.category.children.all()
