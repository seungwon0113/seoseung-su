import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from config.utils.setup_test_method import TestSetupMixin
from products.models import Product, ProductImage
from users.models import User


@pytest.mark.django_db
class TestProductCreateView(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()

    def test_product_create_get_authenticated_admin(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-create')
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'image_form' in response.context
        assert '상품 등록' in response.context['title']

    def test_product_create_get_unauthenticated(self) -> None:
        url = reverse('product-create')
        response = self.client.get(url)
        assert response.status_code == 302  # 리다이렉트

    def test_product_create_get_authenticated_customer(self) -> None:
        self.client.force_login(self.customer_user)
        url = reverse('product-create')
        response = self.client.get(url)
        assert response.status_code == 403  # Forbidden

    def test_product_create_post_valid_data(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-create')
        
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        
        response = self.client.post(url, form_data)
        assert response.status_code == 302  # 리다이렉트
        assert Product.objects.filter(name='테스트 상품').exists()

    def test_product_create_post_with_images(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-create')
        
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        
        image1 = SimpleUploadedFile(
            "test_image1.jpg",
            b"file_content1",
            content_type="image/jpeg"
        )
        image2 = SimpleUploadedFile(
            "test_image2.jpg",
            b"file_content2",
            content_type="image/jpeg"
        )
        
        files = {
            'image': [image1, image2]
        }
        
        response = self.client.post(url, {**form_data, **files})
        assert response.status_code == 302  # 리다이렉트
        
        product = Product.objects.get(name='테스트 상품')
        assert product.image.count() == 2

    def test_product_create_post_invalid_data(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-create')
        
        form_data = {
            'name': '',  # 빈 이름
            'description': '테스트 상품 설명',
            'price': -100,  # 음수 가격
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        
        response = self.client.post(url, form_data)
        assert response.status_code == 200  # 폼 에러로 인해 다시 렌더링
        assert not Product.objects.filter(description='테스트 상품 설명').exists()


@pytest.mark.django_db
class TestProductUpdateView:
    def setup_method(self) -> None:
        self.client = Client()
        self.admin_user = User.objects.create(
            role="admin",
            email="admin@admin.com",
            password="create_test_admin",
            username="admin_user",
            personal_info_consent=True,
            terms_of_use=True,
            phone_number="01012345678"
        )
        self.customer_user = User.objects.create(
            role="customer",
            email="customer@customer.com",
            password="create_test_customer",
            username="customer_user",
            personal_info_consent=True,
            terms_of_use=True,
            phone_number="01087654321"
        )
        self.product = Product.objects.create(
            user=self.admin_user,
            name="기존 상품",
            description="기존 상품 설명",
            price=5000,
            stock=50,
            is_live=True,
            is_sold=False
        )

    def test_product_update_get_authenticated_admin(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'form' in response.context
        assert 'image_form' in response.context
        assert 'product' in response.context
        assert '상품 수정' in response.context['title']

    def test_product_update_get_unauthenticated(self) -> None:
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        assert response.status_code == 302  # 리다이렉트

    def test_product_update_get_authenticated_customer(self) -> None:
        self.client.force_login(self.customer_user)
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        assert response.status_code == 403  # Forbidden

    def test_product_update_post_valid_data(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        
        form_data = {
            'name': '수정된 상품',
            'description': '수정된 상품 설명',
            'price': 15000,
            'stock': 200,
            'is_live': False,
            'is_sold': True
        }
        
        response = self.client.post(url, form_data)
        assert response.status_code == 302  # 리다이렉트
        
        self.product.refresh_from_db()
        assert self.product.name == '수정된 상품'
        assert self.product.price == 15000
        assert self.product.stock == 200
        assert not self.product.is_live
        assert self.product.is_sold

    def test_product_update_post_with_new_images(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        
        form_data = {
            'name': '수정된 상품',
            'description': '수정된 상품 설명',
            'price': 15000,
            'stock': 200,
            'is_live': True,
            'is_sold': False
        }
        
        image = SimpleUploadedFile(
            "new_image.jpg",
            b"new_file_content",
            content_type="image/jpeg"
        )
        
        files = {
            'image': [image]
        }
        
        response = self.client.post(url, {**form_data, **files})
        assert response.status_code == 302  # 리다이렉트
        
        # 새 이미지가 추가되었는지 확인
        assert self.product.image.count() == 1

    def test_product_update_post_invalid_data(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-update', kwargs={'pk': self.product.pk})
        
        form_data = {
            'name': '',  # 빈 이름
            'description': '수정된 상품 설명',
            'price': -100,  # 음수 가격
            'stock': 200,
            'is_live': True,
            'is_sold': False
        }
        
        response = self.client.post(url, form_data)
        assert response.status_code == 200  # 폼 에러로 인해 다시 렌더링
        
        # 상품이 수정되지 않았는지 확인
        self.product.refresh_from_db()
        assert self.product.name == '기존 상품'  # 원래 이름 유지

    def test_product_update_nonexistent_product(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-update', kwargs={'pk': 99999})
        response = self.client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestDeleteProductImageView:
    def setup_method(self) -> None:
        self.client = Client()
        self.admin_user = User.objects.create(
            role="admin",
            email="admin@admin.com",
            password="create_test_admin",
            username="admin_user",
            personal_info_consent=True,
            terms_of_use=True,
            phone_number="01012345678"
        )
        self.customer_user = User.objects.create(
            role="customer",
            email="customer@customer.com",
            password="create_test_customer",
            username="customer_user",
            personal_info_consent=True,
            terms_of_use=True,
            phone_number="01087654321"
        )
        self.product = Product.objects.create(
            user=self.admin_user,
            name="테스트 상품",
            description="테스트 상품 설명",
            price=10000,
            stock=100,
            is_live=True,
            is_sold=False
        )

    def test_delete_image_authenticated_admin(self) -> None:
        self.client.force_login(self.admin_user)
        
        # 테스트용 이미지 생성
        from django.core.files.uploadedfile import SimpleUploadedFile
        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        product_image = ProductImage.objects.create(image=image_file)
        self.product.image.add(product_image)
        
        url = reverse('product-delete-image', kwargs={'image_id': product_image.id})
        response = self.client.delete(url)
        
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert not ProductImage.objects.filter(id=product_image.id).exists()

    def test_delete_image_unauthenticated(self) -> None:
        url = reverse('product-delete-image', kwargs={'image_id': 1})
        response = self.client.delete(url)
        assert response.status_code == 302  # 리다이렉트

    def test_delete_image_authenticated_customer(self) -> None:
        self.client.force_login(self.customer_user)
        url = reverse('product-delete-image', kwargs={'image_id': 1})
        response = self.client.delete(url)
        assert response.status_code == 403  # Forbidden

    def test_delete_nonexistent_image(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-delete-image', kwargs={'image_id': 99999})
        response = self.client.delete(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestProductListView:
    def setup_method(self) -> None:
        self.client = Client()
        self.admin_user = User.objects.create(
            role="admin",
            email="admin@admin.com",
            password="create_test_admin",
            username="admin_user",
            personal_info_consent=True,
            terms_of_use=True,
            phone_number="01012345678"
        )
        self.customer_user = User.objects.create(
            role="customer",
            email="customer@customer.com",
            password="create_test_customer",
            username="customer_user",
            personal_info_consent=True,
            terms_of_use=True,
            phone_number="01087654321"
        )

    def test_product_list_get_authenticated_admin(self) -> None:
        self.client.force_login(self.admin_user)
        
        Product.objects.create(
            user=self.admin_user,
            name="상품 1",
            description="상품 1 설명",
            price=10000,
            stock=100,
            is_live=True,
            is_sold=False
        )
        Product.objects.create(
            user=self.admin_user,
            name="상품 2",
            description="상품 2 설명",
            price=20000,
            stock=50,
            is_live=True,
            is_sold=False
        )
        
        url = reverse('product-list')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert 'products' in response.context
        assert '상품 목록' in response.context['title']
        assert len(response.context['products']) == 2

    def test_product_list_get_unauthenticated(self) -> None:
        url = reverse('product-list')
        response = self.client.get(url)
        assert response.status_code == 302  # 리다이렉트

    def test_product_list_get_authenticated_customer(self) -> None:
        self.client.force_login(self.customer_user)
        url = reverse('product-list')
        response = self.client.get(url)
        assert response.status_code == 403  # Forbidden

    def test_product_list_empty(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-list')
        response = self.client.get(url)
        
        assert response.status_code == 200
        assert 'products' in response.context
        assert len(response.context['products']) == 0
