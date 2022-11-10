from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
    })

@login_required
def my_listings(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(user=request.user)
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


@login_required
def category_name(request, category_name):
    listings = Listing.objects.filter(category = category_name, is_active=True)
    return render(request, "auctions/category_name.html", {
        "listings": listings,
        "category_name": category_name
    })

@login_required 
def create(request):
    if request.method == "POST":
        user = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        start_bid = Bid(bid=request.POST["start_bid"], user=user)
        start_bid.save()
        image_url = request.POST["image_url"]
        new_listing = Listing(
            user = user, 
            title = title, 
            description = description,
            category = category,
            start_bid = start_bid,
            image_url = image_url,
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return  render(request, "auctions/create.html")

def category(request):
    categories = Listing.objects.all().values_list('category', flat=True).distinct()
    return render(request, "auctions/category.html", {
        "categories": categories
    })

@login_required
def listing(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id) # pk means "primary key"
    isInWatchList = False
    isOwner = False 
    if user in listing.watchlist.all():
        isInWatchList = True
    if user == listing.user:
        isOwner = True
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "isInWatchList": isInWatchList,
        "isOwner": isOwner,
        "comments": listing.commentlistings.all(),
        "user": user
    })


@login_required 
def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required 
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def watchlist(request):
    user = request.user
    listings = user.watchlists.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings.filter(is_active=True)
    })

@login_required
def close_bid(request, listing_id):
    pass

@login_required
def comment(request, listing_id):
    user = request.user
    comment = request.POST["comment"]
    listing = Listing.objects.get(pk=listing_id)
    new_comment = Comment(
        user=user,
        comment=comment,
        listing=listing
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def new_bid(request, listing_id):
    new_bid_price = float(request.POST["new_bid"])
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    if_update_bid = False
    if listing.start_bid.bid < new_bid_price:
        new_bid = Bid(user=user, bid=new_bid_price)
        new_bid.save()
        listing.start_bid = new_bid 
        listing.save()
        if_update_bid = True
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Update New Bid Price",
            "if_update_bid": if_update_bid
        })
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": "Please Enter a Bid Higher Than Current Price",
        "if_update_bid": if_update_bid
    })
         
@login_required 
def remove_active(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.is_active = False
    listing.save()
    if_closed = True 
    return render(request, "auctions/listing.html", {
        "listing": listing, 
        "close_message": "Closed the Listing",
        "if_closed": if_closed
    })

