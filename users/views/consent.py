from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class PersonalInfoConsent(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'users/personal_info_consent.html')