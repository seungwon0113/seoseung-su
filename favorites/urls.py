from django.urls import path

from favorites.views.views import FavoritesView

urlpatterns = [
    path('', FavoritesView.as_view(), name='favorite-list'),
]