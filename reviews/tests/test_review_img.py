import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from config.utils.setup_test_method import TestSetupMixin
from reviews.forms.review_create import MultipleFileField


@pytest.mark.django_db
class TestReviewImg(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()
        self.setup_test_products_data()
        self.setup_test_reviews_data()

    def test_clean_with_multiple_files(self) -> None:
        # Given: 더미 파일 2개 준비
        file1 = SimpleUploadedFile("file1.txt", b"hello world", content_type="text/plain")
        file2 = SimpleUploadedFile("file2.txt", b"second file", content_type="text/plain")

        field = MultipleFileField()

        # When: 여러 파일로 clean 호출
        cleaned_files = field.clean([file1, file2])

        # Then: 리스트로 반환됨
        assert isinstance(cleaned_files, list)
        assert len(cleaned_files) == 2
        assert cleaned_files[0].name == "file1.txt"

    def test_clean_with_single_file(self) -> None:
        file = SimpleUploadedFile("single.txt", b"only one", content_type="text/plain")
        field = MultipleFileField()

        cleaned_file = field.clean(file)
        if isinstance(cleaned_file, list):
            cleaned_file = cleaned_file[0]  # list인 경우 첫 번째 파일 사용

        assert cleaned_file is not None
        assert cleaned_file.name == "single.txt"

    def test_clean_with_no_file(self) -> None:
        field = MultipleFileField(required=False)
        result = field.clean(None)
        assert result is None

    def test_clean_invalid_type_raises_error(self) -> None:
        field = MultipleFileField()
        with pytest.raises(ValidationError):
            field.clean("not_a_file")