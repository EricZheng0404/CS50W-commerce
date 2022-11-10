from django.conf import settings
from django.urls import path
from django.conf.urls.static import static 

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("category", views.category, name="category"),
    path("category/<str:category_name>", views.category_name, name="category_name"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_active/<int:listing_id>", views.remove_active, name="remove_active"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("new_bid/<int:listing_id>", views.new_bid, name="new_bid")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
