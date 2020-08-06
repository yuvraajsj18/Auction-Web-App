from django.contrib import admin

from .models import Bids, Comments, Listings, User, Categories

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)

class ListingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'active')

class BidsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'price')

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'comment', 'datetime')

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Categories, CategoriesAdmin)
