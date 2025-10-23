from django.urls import path

from inquire.views.views import InquireSuccessView, InquireView

urlpatterns = [
    path('', InquireView.as_view(), name='inquire'),
    path('success/', InquireSuccessView.as_view(), name='inquire_success'),
]