from django.db.models import Max

from .models import Auctions, Bid



def offer_is_valid(offer, auction, bid):
    """
    Compare values offer with initial or current bid. 
    If offer is greater than intitial bid and greater than any bids
    it will return TRUE.
    """
    if (offer >= auction.initial_bid) and (bid is None or offer > bid):
        return True
    return False

def max_or_init_bid(auction, bid):
    """
    Check if an auction has already been bidded on or not. 
    If no bids has been found, return initial auction's bid.
    Else if there is one bids return max bid objects, being the last one saved.   
    Used to display a value in fields like bid field or current highest bid. 
    """
    if not bid.exists():
        return auction.initial_bid
    else:
        bid = Bid.objects.filter(auction=auction).aggregate(Max('bid'))['bid__max']
    return bid

