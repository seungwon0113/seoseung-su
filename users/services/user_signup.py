from typing import Any

from django.contrib.auth import login
from django.http import HttpRequest

from users.models import User


class UserService:
    @staticmethod
    def create_and_login_user(
        request: HttpRequest,
        cleaned_data: dict[str, Any]
    ) -> User:
        user = User.objects.create_user(
            username=cleaned_data["username"],
            email=cleaned_data["email"],
            password=cleaned_data["password"],
            personal_info_consent=cleaned_data["personal_info_consent"],
            phone_number=cleaned_data["phone_number"]
            # 기타 필드
        )
        login(request, user)
        return user