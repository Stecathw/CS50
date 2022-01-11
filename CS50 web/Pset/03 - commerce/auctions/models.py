from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
   
    
# Class auction listings
class Auctions(models.Model):
    """
    An auction is a listing of a sold item by a registered user.
    It has :
    a name, 
    an initial price, 
    a current price, 
    a description,      
    an image (url), 
    a date of creation,
    and an opened/closed status.
    
    It is related to :
    a category,
    a user as the seller,
    a winner of auction once auction is closed by the seller.
    
    """
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300, null=True)
    initial_bid = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)
    current_bid = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  
    
    # Relations :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')     
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="buyer")
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
    # For admin purpose
    def __str__(self):
        return f"{self.title} sold by {self.user} | id: {self.pk}"



class Bid(models.Model):
    """
    Bids values and dates related to a listing auction and users.
    """
    bid = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    # Relations :
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bidder')
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    
    # For admin purpose
    def __str__(self):
        return f"{self.bid} on {self.auction} by {self.user}"
 
    
# Class comments on auction listing
class Comments(models.Model):
    """
    Comments linked to auction and user.
    """
    comment = models.TextField(max_length=200)
    date = models.DateField(auto_now_add=True)
    # Relations :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    
    # For admin purpose
    def __str__(self):
        return f"{self.comment} {self.date}"


class Watchlist(models.Model):
    """
    User auctions' favorites.
    """
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="auction")
    watched = models.BooleanField(null=True)

    def __str__(self):
        return f"({self.watcher}) add ({self.auction}) to Watch List"
    
    
class Category(models.Model):
    """
    Catgegory are created by superuser (admin).
    """
    name = models.CharField(max_length=20) 
    
    def __str__(self):
        return f"{self.name}"
    
    
    