from django import forms

from .models import Category


class Create_auction_form(forms.Form):
    """
    Creating a listing auction.
    """
    title = forms.CharField(label="Title :")
    description = forms.CharField(label="Description :", widget=forms.Textarea(attrs={"style":"height:30vh; width:75%"}))
    initial_bid = forms.DecimalField(max_digits=12, decimal_places=2)
    image_url = forms.URLField(label="Image link :")
    category = forms.ModelChoiceField(label="Category :", queryset=Category.objects.all().order_by('name'))
    
class Place_bid_form(forms.Form):
    """
    Bidding on listing auction.
    """
    bid = forms.DecimalField(max_digits=12, decimal_places=2)
    
class Comment_form(forms.Form):
    """
    Commenting on listing auction.
    """
    comment = forms.CharField(widget=forms.Textarea(attrs={"style":"height:5vh; width:25%"}))
