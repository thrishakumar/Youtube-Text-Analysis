from .models import Link
from django.forms import ModelForm


class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ['link']
