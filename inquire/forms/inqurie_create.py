from typing import Any

from django import forms

from inquire.models import Inquire


class InquireForm(forms.ModelForm): # type: ignore
    class Meta:
        model = Inquire
        fields = ['email', 'title', 'content', 'item']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': '문의하실 내용을 자세히 적어주세요.'}),
            'title': forms.TextInput(attrs={'placeholder': '문의 제목을 입력해주세요.'}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            del self.fields['email']
        else:
            self.fields['email'].widget.attrs.update({'placeholder': '답변받을 이메일 주소를 입력해주세요.'})
            self.fields['email'].required = True
        
        if 'email' in self.fields:
            self.fields['email'].label = '이메일'
        self.fields['title'].label = '제목'
        self.fields['content'].label = '문의 내용'
        self.fields['item'].label = '문의 항목'