import pytest
from django.test import Client
from django.urls import reverse

from products.models import Product
from users.models import User


@pytest.mark.django_db
class TestProductDetail:
    def setup_method(self) -> None:
        self.client = Client()
        User.objects.create(role="admin", email="admin@admin.com", password="create_test_admin", username="create_test_user", personal_info_consent=True)

    def test_product_detail_get(self) -> None:

        Product.objects.create(user_id=1, name="test_product", description="test_product", is_live=True, is_sold=False, stock=10, price=10000)
        url = reverse('products-detail', kwargs={'product_name': "test_product"})
        response = self.client.get(url)
        assert response.status_code == 200
