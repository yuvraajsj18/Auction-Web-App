from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new_listing, name="new_listing"),
    path('listing/<int:listing_id>', views.listing, name="listing"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('close', views.close, name="close"),
    path('comments', views.comments, name="comments"),
    path('categories', views.categories, name="categories"),
    path('category/<str:name>', views.category, name='category'),
]
