from typing import Any
from unittest.mock import patch

import pytest
from django.core import mail

from config.utils.setup_test_method import TestSetupMixin
from inquire.services.inquire_user_valid import InquireUserValidService


@pytest.mark.django_db
class TestInquireSendMail(TestSetupMixin):
    def setup_method(self) -> None:
        self.setup_test_user_data()


    def test_send_inquire_email_authenticated_user(self, settings: Any) -> None:
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
        self.client.force_login(self.customer_user)
        user_send_mail = InquireUserValidService.send_inquire_email(
            user=self.customer_user,
            email=self.customer_user.email,
            title="테스트 문의 제목",
            content="테스트 내용입니다.",
            item="delivery"
        )

        assert user_send_mail is True

        assert len(mail.outbox) == 1
        email_message = mail.outbox[0]

        assert "[SeoSeung-Soo 문의]" in email_message.subject
        assert "customer" in email_message.subject
        assert "테스트 내용입니다." in email_message.body

        assert email_message.to == ["seoseungsoo.cp@gmail.com"]
        assert email_message.reply_to == [self.customer_user.email]


    def test_send_inquire_email_anonymous_user(self, settings: Any) -> None:
        settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
        send_mail = InquireUserValidService.send_inquire_email(
            user=None,
            email="guest@example.com",
            title="비회원 문의 테스트",
            content="비회원의 문의 내용",
            item="etc"
        )

        assert send_mail is True
        assert len(mail.outbox) == 1

        email_message = mail.outbox[0]
        assert "비회원" in email_message.subject
        assert "guest@example.com" in email_message.subject
        assert "비회원의 문의 내용" in email_message.body

    def test_send_inquire_email_exception(self, settings: Any) -> None:
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

        with patch('inquire.services.inquire_user_valid.render_to_string', side_effect=Exception("템플릿 오류")):
            result = InquireUserValidService.send_inquire_email(
                user=self.customer_user,
                email=self.customer_user.email,
                title="테스트",
                content="내용",
                item="etc"
            )

        assert result is False

    def test_process_inquire_success(self) -> None:
        user = self.customer_user

        with patch.object(InquireUserValidService, "send_inquire_email", return_value=True) as mock_send_email, \
                patch.object(InquireUserValidService, "create_inquire") as mock_create_inquire:
            success, message = InquireUserValidService.process_inquire(
                user=user,
                email=user.email,
                title="테스트 문의",
                content="내용",
                item="etc"
            )

            assert success is True
            assert "성공" in message
            mock_send_email.assert_called_once()
            mock_create_inquire.assert_called_once()

    def test_process_inquire_email_fail(self) -> None:
        user = self.customer_user

        with patch.object(InquireUserValidService, "send_inquire_email", return_value=False) as mock_send_email:
            success, message = InquireUserValidService.process_inquire(
                user=user,
                email=user.email,
                title="테스트 문의",
                content="내용",
                item="etc"
            )

            assert success is False
            assert "이메일 전송에 실패" in message
            mock_send_email.assert_called_once()

    def test_process_inquire_exception(self) -> None:
        user = self.customer_user

        with patch.object(InquireUserValidService, "send_inquire_email", side_effect=Exception("테스트 예외")):
            success, message = InquireUserValidService.process_inquire(
                user=user,
                email=user.email,
                title="테스트 문의",
                content="내용",
                item="etc"
            )

            assert success is False
            assert "오류가 발생했습니다" in message
            assert "테스트 예외" in message