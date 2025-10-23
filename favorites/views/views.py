from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from favorites.models import Favorite


class FavoritesView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        favorites = Favorite.objects.all()
        context = {"favorites": favorites}
        return render(request, "favorites/favorite_mypage.html", context)