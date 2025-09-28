import pytest
from django.test import Client
from django.urls import reverse

from products.models import Product
from users.models import User


@pytest.mark.django_db
class TestProductDetail:
    def setup_method(self) -> None:
        self.client = Client()
        User.objects.create(role="admin", email="admin@admin.com", password="create_test_admin", username="create_test_user", personal_info_consent=True, terms_of_use=True)

    def test_product_detail_get(self) -> None:
        Product.objects.create(user_id=1, name="test_product", description="test_product", is_live=True, is_sold=False, stock=10, price=10000)
        url = reverse('products-detail', kwargs={'product_name': "test_product"})
        response = self.client.get(url)
        assert response.status_code == 200

    # def test_product_detail_post_name_null_error(self) -> None:
    #     response = self.client.post("/products/add/", {
    #         "user_id": 1,
    #         "name": "",
    #         "description": "test_product",
    #         "is_live": True,
    #         "is_sold": False,
    #         "stock": 10,
    #         "price": 10000
    #     })
    #
    #     assert response.status_code == 200
    #     assert response.content.decode() or "상품 이름이 작성되지 않았습니다." in response.content.decode()

    def test_product_role_not_admin(self) -> None:
        User.objects.create(role="customer", email="customer@customer.com", password="create_test_customer",username="create_test_customer", personal_info_consent=True, phone_number="0123456789", terms_of_use=True)
        customer_user = User.objects.get(username="create_test_customer")
        Product.objects.create(user_id=customer_user.id, name="test_customer_product", description="test_customer_product", is_live=True, is_sold=False, stock=10, price=10000)

