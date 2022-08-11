from django.contrib import admin

from .models import Profile, Comment, Answer, Activity, Message
# Register your models here.

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Answer)
admin.site.register(Activity)
admin.site.register(Message)
