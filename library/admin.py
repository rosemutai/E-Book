from django.contrib import admin
from .models import Genre, Language, Book, Member, Borrower, Reviews, BorrowedBook

# Register your models here.
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Borrower)
admin.site.register(Reviews)
admin.site.register(BorrowedBook)

