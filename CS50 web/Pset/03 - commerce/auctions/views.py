from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from django.template import RequestContext


from .models import User, Auctions, Bid, Watchlist, Category, Comments
from .forms import Create_auction_form, Place_bid_form, Comment_form


from .util import offer_is_valid, max_or_init_bid


def index(request):
    
    """
    Index render all active listings for both authenticated and unauthenticated users.
    For loged in users, it will also take in account watched auctions, 
    rendering them with a yellow star fav icon.
    """
    try:
        # Make a selection here if user is authenticated or not to make lighter query on db
        user = User.objects.get(pk=request.user.id)
        watchlist = Watchlist.objects.filter(watcher=user)
    except:
        watchlist = Watchlist.objects.all()
    auctions = Auctions.objects.filter(is_active="True")  
    return render(request, "auctions/index.html", {
        "auctions" : auctions,
        "watchlist": watchlist,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create_auction(request):
    """
    Allow user to create and open an active auction.
    By default, once created and saved, listing auction will be active and viewable by any users
    until closed.
    """
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        form = Create_auction_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            description = form.cleaned_data["description"]
            initial_bid = form.cleaned_data["initial_bid"]
            image = form.cleaned_data["image_url"]
            category = form.cleaned_data['category']
            try:
                auction = Auctions.objects.create(
                    title = title,
                    description = description,
                    image = image,
                    initial_bid = initial_bid, 
                    user = user,
                    category = category,            
                )   
                auction.save()       
                return HttpResponseRedirect(reverse("index"))
            except:
                raise Http404("Internal server error, can't reach database !")
    return render(request, "auctions/create_auction.html", {
        "form": Create_auction_form()
    })
    
    
def auction_page(request, auction_id):  
    """
    Define the listing auction page rendering all informations about it.  
    Accessible to all users. 
    But comments section and bidding on it will only be accessible to loged in users.  
    """
    try:  
        auction = Auctions.objects.get(pk=auction_id) 
        bid = Bid.objects.filter(auction=auction).order_by('date')
        is_watched = Watchlist.objects.filter(auction=auction_id, watcher=request.user.id)
        comments = Comments.objects.filter(auction=auction_id)
        return render(request, "auctions/auction_page.html", {
            "auction": auction,        
            "form_bid": Place_bid_form(initial={'bid':auction.current_bid}),
            "form_comment": Comment_form(),
            "bid": max_or_init_bid(auction, bid),
            "watched": is_watched.values('watched'),
            "comments": comments,
            "bids": bid
        })
    except:
        raise Http404("Internal server error, can't reach database !")


@login_required
def comment(request, auction_id):
    """
    Allow loged in users to comment on a listing auction page.
    """
    if request.method == "POST":
        auction = Auctions.objects.get(pk=auction_id)
        user = User.objects.get(pk=request.user.id)
        form = Comment_form(request.POST)
        if form.is_valid():
            text = form.cleaned_data['comment']
            try:
                comment = Comments.objects.create(
                    comment = text,
                    user=user,
                    auction=auction,
                )
                comment.save()
            except:
                raise Http404("Internal server error, can't reach database !")            
    return HttpResponseRedirect(reverse('auction_page', args=[auction_id]))

@login_required
def close_auction(request, auction_id):
    """
    Allow loged in user owning the listing auction to close it.
    The auction will be no longer active neither viewable (apart from the django admin page).
    It register the auction winner.    
    """
    auction = Auctions.objects.get(pk=auction_id)
    # The lastest bid is the highest bid registered therefore last() is used as a simple method to find winner
    # Not the robustest method, cf django admin
    highest_bid = Bid.objects.filter(auction=auction).last() 
    try:
        auction.is_active = False
        if highest_bid is None:
            auction.winner = auction.user
        else:
            auction.winner = highest_bid.user
        print(auction.winner)
        auction.save()
    except:
        raise Http404("Internal server error, can't reach database !")
    return HttpResponseRedirect(reverse('auction_page', args=[auction_id]))

@login_required
def place_bid(request, auction_id):
    """
    Loged in user as interested buyer can place bid on auction.
    If user place a bid, it will automaticly add the listing to its watchlist 
    in order to easely keep track of it.
    """
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        auction = Auctions.objects.get(pk=auction_id)
        watchlist = Watchlist.objects.filter(watcher=user)
        bid_form = Place_bid_form(request.POST)
        bid = Bid.objects.filter(auction=auction).aggregate(Max('bid'))['bid__max']
        if bid_form.is_valid():
            offer = bid_form.cleaned_data["bid"] 
            if offer_is_valid(offer, auction, bid): 
                try:           
                    bid = Bid.objects.create(
                        bid = offer,
                        user = user,
                        auction = auction,
                    )
                    auction.current_bid = offer
                    # Automaticly add the auction to the user watchlist.
                    if not watchlist.filter(auction=auction).exists():
                        watchlist = Watchlist.objects.create(
                            watcher= user,
                            auction= auction, 
                            watched=True
                        )
                        watchlist.save()
                    auction.save()
                    bid.save()
                    messages.success(request, f"You have bidded {offer} $ on {auction.title}.")
                    return HttpResponseRedirect(reverse("auction_page", args=[auction_id]))
                except:
                    raise Http404("Internal server error, can't reach database !")       
    messages.error(request, "Your offer should be higher to current bid.")
    return HttpResponseRedirect(reverse("auction_page", args=[auction_id]))


@login_required
def watchlist(request):
    """
    Render the user watched listings.
    """
    user = User.objects.get(pk=request.user.id)
    watchlist = Watchlist.objects.filter(watcher=user)    
    auctions_id = watchlist.values('auction')    
    user_auctions = Auctions.objects.filter(pk__in=auctions_id)    
    if watchlist is None:
        return HttpResponseRedirect("index")
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_auctions,
    })     


@login_required
def add_to_watchlist(request, auction_id):
    """
    Allow loged in user to add a listing to his watchlist.
    """
    user = User.objects.get(pk=request.user.id)
    auction = Auctions.objects.get(pk=auction_id)
    watchlist = Watchlist.objects.filter(watcher=user)
    if not watchlist.filter(auction=auction).exists():
        try:
            watchlist = Watchlist.objects.create(
                watcher= user,
                auction= auction, 
                watched=True
            )
            watchlist.save()
            messages.success(request, f"{auction.title} successfully added to watchlist !")
            return HttpResponseRedirect(reverse("auction_page", args=[auction_id])) 
        except:
            raise Http404("Internal server error, can't reach database !")      
    messages.error(request, f"{auction.title} already in your watchlist !")
    return HttpResponseRedirect(reverse("auction_page", args=[auction_id]))


@login_required
def remove_from_watchlist(request, auction_id):
    """
    Allow user to remove a listing from his watchlist.
    From auction page directly.
    """
    user = User.objects.get(pk=request.user.id)
    auction = Auctions.objects.get(pk=auction_id)  
    try:
        watchlist = Watchlist.objects.filter(watcher=user, auction=auction_id, watched=True)
        watchlist.delete()
    except:
        raise Http404("Internal server error, can't reach database !")
    messages.success(request, f"{auction.title} successfully removed from watchlist !")
    return HttpResponseRedirect(reverse("auction_page", args=[auction_id]))


@login_required
def remove_from_watchlist_bis(request, auction_id):
    """
    Same as "remove_from_watchlist", but from user's watchlist.
    """
    user = User.objects.get(pk=request.user.id)
    auction = Auctions.objects.get(pk=auction_id)  
    try:
        watchlist = Watchlist.objects.filter(watcher=user, auction=auction_id, watched=True)
        watchlist.delete()
    except:
        raise Http404("Internal server error, can't reach database !")
    messages.success(request, f"{auction.title} successfully removed from watchlist !")
    return HttpResponseRedirect(reverse("watchlist"))
  
 
def category(request, category):
    """
    Allow user to filter by category and active listings.
    """
    category_id = Category.objects.filter(name=category).values_list('id', flat=True).first()
    auctions = Auctions.objects.filter(is_active=True, category=category_id)
    return render(request, "auctions/category.html", {
        "auctions": auctions,
        "cat": category,
    }) 

 