from django.contrib import admin
from .models import User, Auctions, Bid, Comments, Watchlist, Category

# Register your models here.
admin.site.register(Auctions)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Category)
