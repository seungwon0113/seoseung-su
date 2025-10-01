from django.urls import path

from categories.views.list_category import CategoryListView

urlpatterns = [
    path('list/', CategoryListView.as_view(), name='category-list'),
]