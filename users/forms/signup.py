from typing import Any, cast

from django import forms

from users.models import User


class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(widget=forms.TextInput, required=True)
    phone1 = forms.CharField(widget=forms.TextInput, required=False)
    phone2 = forms.CharField(widget=forms.TextInput, required=False)
    phone3 = forms.CharField(widget=forms.TextInput, required=False)
    personal_info_consent = forms.BooleanField()
    terms_of_use = forms.BooleanField()
    sns_consent_to_receive = forms.BooleanField(required=False)
    email_consent_to_receive = forms.BooleanField(required=False)

    def clean(self) -> dict[str, Any]:
        cleaned_data = cast(dict[str, Any], super().clean())
        pwd = cleaned_data.get("password")
        pwd_confirm = cleaned_data.get("passwordConfirm")
        if pwd and pwd_confirm and pwd != pwd_confirm:
            self.add_error("passwordConfirm", "비밀번호가 일치하지 않습니다.")
        
        # 휴대폰 번호 처리 (phone1, phone2, phone3을 합쳐서 phone_number 생성)
        phone1 = cleaned_data.get("phone1", "")
        phone2 = cleaned_data.get("phone2", "")
        phone3 = cleaned_data.get("phone3", "")
        phone_number = cleaned_data.get("phone_number", "")
        
        # phone_number가 없으면 phone1, phone2, phone3을 합쳐서 생성
        if not phone_number and phone1 and phone2 and phone3:
            phone_number = phone1 + phone2 + phone3
            cleaned_data["phone_number"] = phone_number
        
        # 휴대폰 번호 필수 체크
        if not phone_number:
            self.add_error("phone_number", "휴대폰 번호를 입력해주세요.")
        elif len(phone_number) != 11:
            self.add_error("phone_number", "휴대폰 번호는 11자리여야 합니다.")
        elif User.objects.filter(phone_number=phone_number).exists():
            self.add_error("phone_number", "이미 등록된 휴대폰 번호입니다.")
        
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
