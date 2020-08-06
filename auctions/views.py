from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import NewListingForm, BidForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listings.objects.all()
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return render(request, "auctions/index.html", {
                'listings': Listings.objects.all()
            })
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


# Creates a new listing
@login_required(redirect_field_name="", login_url=reverse_lazy('auctions:login'))
def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)

        if not form.is_valid():
            return render(request, 'auctions/newlisting.html', {"form": form})

        if form.cleaned_data['category']:
            try:
                # if category already exists then use that
                category = Categories.objects.get(
                    name=form.cleaned_data['category'])
            except Categories.DoesNotExist:
                # else create new
                category = Categories(name=form.cleaned_data['category'])
        else:
            try:
                # if no name provided check if Not Specified category exist
                category = Categories.objects.get(name="Not Specified")
            except Categories.DoesNotExist:
                # otherwise make a new Not Specified Category
                category = Categories()

        category.save()
        new_product_listing = Listings(user=request.user, title=form.cleaned_data['title'], description=form.cleaned_data[
                                       'description'], current_price=form.cleaned_data['current_price'], category=category)

        if form.cleaned_data['image_url']:
            new_product_listing.image_url = form.cleaned_data['image_url']

        new_product_listing.save()

        return HttpResponseRedirect(reverse('auctions:listing', args=(new_product_listing.id,)))

    else:
        return render(request, 'auctions/newlisting.html')


def listing(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)

    try:
        if request.user.is_authenticated:
            watchlist = request.user.watchlist.get(pk=listing_id)
        else:
            watchlist = None
    except Listings.DoesNotExist:
        watchlist = None

    # make a bid
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        if not bid_form.is_valid():
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "watchlist": watchlist,
                "bid_form": bid_form,
                "comments": listing.comments.all(),
            })

        # add bid in database
        bid = Bids(user=request.user, listing=listing,
                   price=bid_form.cleaned_data['price'])
        # save and check status
        if bid.save() is None:
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "watchlist": watchlist,
                "bid_form": bid_form,
                "bid_error": "Make a bid higher than current price",
                "comments": listing.comments.all(),
            })

    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "watchlist": watchlist,
        "bid_form": BidForm(),
        "comments": listing.comments.all(),
    })


@login_required(redirect_field_name="", login_url=reverse_lazy('auctions:login'))
def watchlist(request):
    if request.method == "POST":
        watchlist_option = str(request.POST["watchlist_option"])
        listing_id = int(request.POST["listing_id"])

        try:
            listing = request.user.watchlist.get(pk=listing_id)
        except Listings.DoesNotExist:
            listing = Listings.objects.get(pk=listing_id)

        if watchlist_option == "remove":
            request.user.watchlist.remove(listing)
        elif watchlist_option == "add":
            request.user.watchlist.add(listing)

        return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id,)))
    else:
        return render(request, 'auctions/watchlist.html', {
            "watchlist": request.user.watchlist.all(),
        })


@login_required(redirect_field_name="", login_url=reverse_lazy('auctions:login'))
def close(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listings.objects.get(pk=listing_id)

        highest_bid = listing.bids.get(price=listing.current_price)

        listing.active = False
        listing.winner = highest_bid.user
        listing.save()

        return HttpResponseRedirect(reverse('auctions:listing', args=(listing_id, )))
    else:
        return HttpResponseRedirect(reverse('auctions:index'))


@login_required(redirect_field_name="", login_url=reverse_lazy('auctions:login'))
def comments(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        listing = Listings.objects.get(pk=request.POST['listing_id'])
        if not comment_form.is_valid():
            return render(request, 'auctions/listing.html', {
                "listing": listing,
                "watchlist": request.user.watchlist.get(pk=listing.id),
                "bid_form": BidForm(),
                "comments": listing.comments.all(),
                "comment_form": comment_form,
            })

        comment_text = comment_form.cleaned_data['comment']
        comment = Comments(user=request.user,
                           listing=listing, comment=comment_text)
        comment.save()

        return HttpResponseRedirect(reverse('auctions:listing', args=(listing.id,)))
    else:
        return HttpResponseRedirect(reverse('auctions:index'))


@login_required(redirect_field_name="", login_url=reverse_lazy('auctions:login'))
def categories(request):
    nonempty_categories = Categories.objects.all()
    nonempty_categories = [
        item for item in nonempty_categories if len(item.listings.all()) > 0]

    return render(request, 'auctions/categories.html', {
        "categories": sorted(nonempty_categories, key=lambda category: category.name),
    })


def category(request, name):
    category = Categories.objects.get(name=name)

    return render(request, 'auctions/category.html', {
        'category': category,
        'category_listings': category.listings.all(),
    })
