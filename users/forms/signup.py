from typing import Any, cast

from django import forms

from users.models import User


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(widget=forms.TextInput)
    personal_info_consent = forms.BooleanField()

    def clean(self) -> dict[str, Any]:
        cleaned_data = cast(dict[str, Any], super().clean())
        pwd = cleaned_data.get("password")
        pwd_confirm = cleaned_data.get("passwordConfirm")
        if pwd and pwd_confirm and pwd != pwd_confirm:
            self.add_error("passwordConfirm", "비밀번호가 일치하지 않습니다.")
        return cleaned_data

    def clean_username(self) -> str:
        username = cast(str, self.cleaned_data.get("username"))
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 존재하는 아이디입니다.")
        return username

    def clean_email(self) -> str:
        email = cast(str, self.cleaned_data.get("email"))
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 가입된 이메일입니다.")
        return email

    def clean_phone_number(self) -> str:
        phone_number = cast(str, self.cleaned_data.get("phone_number"))
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("이미 등록된 휴대폰 번호입니다.")
        return phone_number