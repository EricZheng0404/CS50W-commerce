from django.forms import ModelForm
from .models import Listing, Comment, Bid

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        exclude = ['user']

