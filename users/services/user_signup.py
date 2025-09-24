from typing import Any

from django.db import IntegrityError
from django.http import HttpRequest

from users.models import User


class UserService:
    @staticmethod
    def create_and_login_user(
        request: HttpRequest,
        cleaned_data: dict[str, Any]
    ) -> User:
        try:
            request.user = User.objects.create_user(
                username=cleaned_data["username"],
                email=cleaned_data["email"],
                password=cleaned_data["password"],
                personal_info_consent=cleaned_data["personal_info_consent"],
                phone_number=cleaned_data["phone_number"],
                terms_of_use=cleaned_data.get("terms_of_use", False),
                sns_consent_to_receive=cleaned_data.get("sns_consent_to_receive", False),
                email_consent_to_receive=cleaned_data.get("email_consent_to_receive", False)
            )
            return request.user
        except IntegrityError:
            raise ValueError("이미 존재하는 아이디 또는 이메일입니다.")

#TODO: https://developers.kakao.com/tool/template-builder/app/1315204/template
'''카카오톡 배송목록 메세지 전달 추가 예정'''

