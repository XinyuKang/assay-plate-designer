from django.forms import ModelForm
from .models import Plate


class PlateForm(ModelForm):
    class Meta:
        model = Plate
        fields = "__all__"