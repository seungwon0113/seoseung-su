from typing import cast
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.urls import reverse
from django.utils.datastructures import MultiValueDict

from config.utils.setup_test_method import TestSetupMixin
from products.forms.product_form import MultipleFileField, ProductImageForm
from products.models import ProductImage


@pytest.mark.django_db
class TestProductImageForm(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()

    def test_product_image_form_valid_data(self) -> None:
        image = cast(UploadedFile, SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        ))
        files: MultiValueDict[str, UploadedFile] = MultiValueDict({'image': [image]})
        form = ProductImageForm(data={}, files=files)
        assert form.is_valid()

    def test_multiple_file_field_clean_with_single_file(self) -> None:
        file = SimpleUploadedFile("test.txt", b"file content", content_type="text/plain")
        field = MultipleFileField()
        result = field.clean(file, None)
        assert isinstance(result, SimpleUploadedFile)

    def test_product_image_form_no_image(self) -> None:
        files: MultiValueDict[str, UploadedFile] = MultiValueDict()
        form = ProductImageForm(data={}, files=files)
        assert form.is_valid()

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
        assert form.is_valid()

    def test_product_image_form_invalid_file_type(self) -> None:
        text_file = cast(UploadedFile, SimpleUploadedFile(
            "test.txt",
            b"file_content",
            content_type="text/plain"
        ))
        files: MultiValueDict[str, UploadedFile] = MultiValueDict({'image': [text_file]})
        form = ProductImageForm(data={}, files=files)
        assert form.is_valid()

    def test_admin_image_delete_404(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-delete-image', kwargs={'image_id': 99999})
        response = self.client.delete(url)

        assert response.status_code == 404
        json_response = response.json()
        assert json_response['success'] is False
        assert '찾을 수 없습니다' in json_response['message']

    def test_admin_image_delete_500(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse('product-delete-image', kwargs={'image_id': self.image.id})

        with patch.object(ProductImage, 'delete', side_effect=Exception('강제 예외 발생')):
            response = self.client.delete(url)

        assert response.status_code == 500
        json_response = response.json()
        assert json_response['success'] is False
        assert '삭제 중 오류가 발생했습니다' in json_response['message']