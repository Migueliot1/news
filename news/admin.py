from django.contrib import admin

# Register your models here.
from .models import NewsWebsite, ImageWebsite, Article, Searchables

admin.site.register(NewsWebsite)
admin.site.register(ImageWebsite)
admin.site.register(Article)
admin.site.register(Searchables)
