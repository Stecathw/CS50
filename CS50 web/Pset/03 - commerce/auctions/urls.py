from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("index", views.index, name="index"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("auction_page/<int:auction_id>", views.auction_page, name="auction_page"),
    path("close_auction/<int:auction_id>", views.close_auction, name="close_auction"),
    path("comment/<int:auction_id>", views.comment, name="comment"),
    path("place_bid/<int:auction_id>", views.place_bid, name="place_bid"),
    path("add_to_watchlist/<int:auction_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:auction_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("remove_from_watchlist_bis/<int:auction_id>", views.remove_from_watchlist_bis, name="remove_from_watchlist_bis"),
    path("watchlist", views.watchlist, name="watchlist"),    
    path("category/<str:category>", views.category, name="category"),
]
