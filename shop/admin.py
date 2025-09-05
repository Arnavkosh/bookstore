from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','price','stock','created')
    list_filter=('created',)
    search_fields=('title','author','description')
    prepopulated_fields={'slug':('title',)}
