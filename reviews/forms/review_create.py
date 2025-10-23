from typing import Any, List, Union, cast

from django import forms
from django.core.files.uploadedfile import UploadedFile

from reviews.models import Review, ReviewComment


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data: Any, initial: Any = None) -> Union[List[UploadedFile], UploadedFile, None]:
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ReviewForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': '상품에 대한 리뷰를 작성해주세요 (최소 10자 이상)',
                'rows': 5,
                'maxlength': 1000
            }),
            'rating': forms.RadioSelect(
                choices=[(i, f'{i}점') for i in range(1, 6)],
                attrs={
                    'class': 'rating-input'
                }
            )
        }
        labels = {
            'content': '리뷰 내용',
            'rating': '평점'
        }
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # rating 필드에 기본값 5점 설정
        if not self.instance.pk and 'rating' not in self.initial:
            self.initial['rating'] = 5
    
    def clean_rating(self) -> int:
        rating = cast(int, self.cleaned_data.get('rating'))
        if rating < 1 or rating > 5:
            raise forms.ValidationError("평점은 1점부터 5점까지 선택 가능합니다.")
        return rating


class ReviewImageForm(forms.Form):
    image: MultipleFileField = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-file',
            'accept': 'image/*',
            'multiple': True
        }),
        label='리뷰 이미지'
    )


class ReviewCommentForm(forms.ModelForm):  # type: ignore[type-arg]
    class Meta:
        model = ReviewComment
        fields = ['content', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-textarea comment-textarea',
                'placeholder': '댓글을 입력하세요 (최대 500자)',
                'rows': 3,
                'maxlength': 500
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'comment-public-checkbox'
            })
        }
        labels = {
            'content': '',
            'is_published': '공개 댓글'
        }
    
    def clean_content(self) -> str:
        content = cast(str, self.cleaned_data.get('content'))
        if content is None:
            content = ''
        if len(content.strip()) < 1:
            raise forms.ValidationError("댓글 내용을 입력해주세요.")
        if len(content) > 500:
            raise forms.ValidationError("댓글은 최대 500자까지 입력 가능합니다.")
        return content