from typing import cast

from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from products.forms.product_form import ProductForm, ProductImageForm


class TestProductForm(TestCase):
    def test_product_form_valid_data(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000.50,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_invalid_price_negative(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': -100,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_product_form_invalid_price_zero(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 0,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_product_form_invalid_stock_negative(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000,
            'stock': -10,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)

    def test_product_form_missing_required_fields(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'price': 10000,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_product_form_clean_price_method(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000.50,
            'stock': 100,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.clean_price(), 10000.50)

    def test_product_form_clean_stock_method(self) -> None:
        form_data = {
            'name': '테스트 상품',
            'description': '테스트 상품 설명',
            'price': 10000,
            'stock': 50,
            'is_live': True,
            'is_sold': False
        }
        form = ProductForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.clean_stock(), 50)


class TestProductImageForm(TestCase):
    def test_product_image_form_valid_data(self) -> None:
        image = cast(UploadedFile, SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        ))
        files: MultiValueDict[str, UploadedFile] = MultiValueDict({'image': [image]})
        form = ProductImageForm(data={}, files=files)
        self.assertTrue(form.is_valid())

    def test_product_image_form_no_image(self) -> None:
        files: MultiValueDict[str, UploadedFile] = MultiValueDict()
        form = ProductImageForm(data={}, files=files)
        self.assertTrue(form.is_valid())

    def test_product_image_form_multiple_images(self) -> None:
        image1 = cast(UploadedFile, SimpleUploadedFile(
            "test_image1.jpg",
            b"file_content1",
            content_type="image/jpeg"
        ))
        image2 = cast(UploadedFile, SimpleUploadedFile(
            "test_image2.jpg",
            b"file_content2",
            content_type="image/jpeg"
        ))
        files: MultiValueDict[str, UploadedFile] = MultiValueDict({'image': [image1, image2]})
        form = ProductImageForm(data={}, files=files)
        self.assertTrue(form.is_valid())

    def test_product_image_form_invalid_file_type(self) -> None:
        text_file = cast(UploadedFile, SimpleUploadedFile(
            "test.txt",
            b"file_content",
            content_type="text/plain"
        ))
        files: MultiValueDict[str, UploadedFile] = MultiValueDict({'image': [text_file]})
        form = ProductImageForm(data={}, files=files)
        # FileField는 파일 타입을 자동으로 검증하지 않으므로 유효할 수 있음
        # 실제 검증은 뷰에서 처리됨
        self.assertTrue(form.is_valid())
