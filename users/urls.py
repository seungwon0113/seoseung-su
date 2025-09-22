from django.urls import path

from users.views import LoginView
from users.views.check_duplicate import CheckDuplicateView
from users.views.signup import SignupView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("check-duplicate/", CheckDuplicateView.as_view(), name="check-duplicate"),
]