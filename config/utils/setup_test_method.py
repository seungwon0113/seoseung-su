from django.test.client import Client

from products.models import Product
from users.models import User


class TestSetupMixin:
    def setup_test_data(self) -> None:
        self.client = Client()
        
        self.admin_user = User.objects.create_user(
            role='admin',
            username='admin',
            email='admin@admin.com',
            password='admin_password',
            personal_info_consent=True,
            terms_of_use=True
        )

        self.user = User.objects.create_user(
            role='customer',
            username='customer',
            email='customer@customer.com',
            password='customer',
            personal_info_consent=True,
            terms_of_use=True
        )
        
        self.product = Product.objects.create(
            user=self.admin_user,
            name='Test Product',
            description='Test Description',
            price=5.00,
            stock=5
        )