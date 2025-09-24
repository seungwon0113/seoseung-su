from django.urls import path

from users.views import LoginView
from users.views.check_duplicate import CheckDuplicateView
from users.views.consent import consent_view
from users.views.kakao_callback import KakaoCallbackView
from users.views.login import LogoutView
from users.views.signup import SignupView
from users.views.social_login import GoogleLoginView, KakaoLoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("consent/", consent_view, name="consent"),
    path("check-duplicate/", CheckDuplicateView.as_view(), name="check-duplicate"),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    path("auth/kakao/", KakaoLoginView.as_view(), name="kakao-login"),
    path("auth/kakao/callback/", KakaoCallbackView.as_view(), name="kakao-callback"),
]