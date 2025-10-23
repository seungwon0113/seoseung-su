from django.urls import path

from categories.views.category import CategoryView

urlpatterns = [
    path('list/', CategoryView.as_view(), name='category-list'),
]