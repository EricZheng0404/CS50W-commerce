from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from regex import F


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Bid(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="bids")
    bid = models.FloatField(blank=False)

    def __str__(self):
        return f"{self.user}: {self.bid}"

class Listing(models.Model):
    user = models.ForeignKey(User,blank=False, on_delete=models.CASCADE, related_name="users") # Must have
    title = models.CharField(max_length=64, blank=False) # Must have
    description = models.TextField()
    category = models.CharField(max_length=64, blank=True, null=True)
    start_bid = models.ForeignKey(Bid,blank=False, on_delete=models.CASCADE, related_name="userbids")
    image_url = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlists", null=True)
    def __str__(self):
        return f"{self.id}: {self.title}"


    def __str__(self):
        return f"{self.id}: {self.title}, {self.start_bid}"


class Comment(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="commentusers")
    listing = models.ForeignKey(Listing, blank=False, on_delete=models.CASCADE, related_name="commentlistings")
    comment = models.TextField(max_length=500)
    
    def __str__(self):
        return f"{self.listing}, {self.user}: {self.comment}"