from django.urls import path

from favorites.views.views import (
    FavoriteCreateView,
    FavoriteDeleteView,
    FavoriteToggleView,
    FavoriteView,
)

urlpatterns = [
    path('', FavoriteView.as_view(), name='favorite-list'),
    path('create/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('toggle/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('delete/', FavoriteDeleteView.as_view(), name='favorite-delete'),
]