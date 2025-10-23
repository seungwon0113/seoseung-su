from django.forms import ModelForm

from favorites.models import Favorite


class FavoriteListForm(ModelForm): # type: ignore
    class Meta:
        model = Favorite
        fields = ('user', 'product', 'is_active')