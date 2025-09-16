from typing import Any

from django import forms


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(widget=forms.TextInput)
    personal_info_consent = forms.BooleanField()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        assert cleaned_data is not None
        pwd = cleaned_data.get("password")
        pwd_confirm = cleaned_data.get("passwordConfirm")
        if pwd and pwd_confirm and pwd != pwd_confirm:
            self.add_error("passwordConfirm", "비밀번호가 일치하지 않습니다.")
        return cleaned_data