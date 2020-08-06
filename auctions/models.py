from django.contrib.auth.models import AbstractUser
from django.db import models

# Represents our user
class User(AbstractUser):
    watchlist = models.ManyToManyField('Listings', blank = True, related_name="watchlist_users")

    def __str__(self):
        return f"{self.username}"


# Represent a product listing
class Listings(models.Model):
    # user who created the listing
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "listings")
    # title of the listing
    title = models.CharField(max_length = 64)
    description = models.CharField(max_length = 280)
    current_price = models.DecimalField(max_digits = 9 ,decimal_places = 2)
    # category
    category = models.ForeignKey('Categories', on_delete = models.CASCADE, related_name="listings")
    image_url = models.URLField(blank = True)
    # store status of listing - open(True) or close(False)
    active = models.BooleanField(default = True)
    # time and date of Creation
    datetime = models.DateTimeField(auto_now_add = True)
    # winner of listing
    winner = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True, related_name="purchased_listings")

    def __str__(self):
        return f"{self.title} by {self.user} at {self.current_price}"


# Represents bids on diffrent listings
class Bids(models.Model):
    # user who bidded this price
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bids")
    # listing on which bid is made
    listing = models.ForeignKey(Listings, on_delete = models.CASCADE, related_name = "bids")
    # price of bid
    price = models.DecimalField(max_digits = 9 ,decimal_places = 2)

    # only save the bid if it follow the desired conditions
    def save(self, *args, **kwargs):
        # bid price should be more than current price of listing and the listing must be active
        if self.listing.current_price > self.price or not self.listing.active:
            return None
        self.listing.current_price = self.price
        self.listing.save()
        print(self.listing.current_price)
        super().save(*args, **kwargs)
        return True


    def __str__(self):
        return f"${self.price} on {self.listing.title} by {self.user}"



# Represents Comments on different product listings
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    listing = models.ForeignKey(Listings, on_delete = models.CASCADE, related_name = "comments")
    comment = models.CharField(max_length = 140)
    datetime = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f"'{self.comment}' on {self.listing.title} by {self.user}"


class Categories(models.Model):
    name = models.CharField(max_length = 64, default = "Not Specified", unique = True)

    def __str__(self):
        return f"Category: {self.name}"

