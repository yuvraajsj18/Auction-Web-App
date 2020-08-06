from django import forms
from .models import Listings, Bids, Comments

class NewListingForm(forms.ModelForm):
    category = forms.CharField(max_length = 64, required=False)
    class Meta:
        model = Listings
        fields = ['title', 'description', 'current_price', 'image_url']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['price']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']