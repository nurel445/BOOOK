from django.contrib import admin

from django.contrib import admin
from .models import Book, User, Review, ReadingList, Follow

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Review)
admin.site.register(ReadingList)
admin.site.register(Follow)
