# Project 2 - Commerce

Design an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

Link to youtube video demo:

https://www.youtube.com/watch?v=-laezbW4N_g


Link to project specifications :

https://cs50.harvard.edu/web/2020/projects/2/commerce/

### Thoughts

Goal was to create a simple auction site, using django models and manipulating objects and instances.

Further improvements could be :
- an historical tab for users to see closed listing.
- a better tracking of winned listing with email sending.
- a better responsive design
- graphism and UI design : more interaction and animations.

### Technical aspects :

- I had to create a django context processor in order to populate catgory dropdown within the layout template and so to make the dropdown available within each of the templates navbar.
- I've used bootstrap to create cards and grids, tootips and navbar. I've tried to make my front end as responsive as I can. But still had some trouble during transitions (screen sizes large to small and small to large).
- I've used django crispy form, to improve forms appearance.
- I've used a little bit of css and javascript to make little animations.

From a wider point of view, I put a lot of efforts into this project and discovered much more aspects. Sometimes little things takes longer than largest fonctionnalities. A well made finished site needs a lot of time and efforts. Therefore I tried my own things from the specifications and it would need a lot more to be really finished and usefull. Even my queries could be better handled, especially the ones about finding the max bid and returning the winner. It works but it could be improved for sure.

### Specifications

Complete the implementation of your auction site. You must fulfill the following requirements:

* Models: Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
* Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
* Active Listings Page: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
* Listing Page: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    ** If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
    ** If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that        have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    ** If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the      winner of the auction and makes the listing no longer active.
    ** If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
* Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.
* Watchlist: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
* Categories: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
* Django Admin Interface: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.
