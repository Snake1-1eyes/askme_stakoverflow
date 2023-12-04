from django.contrib import admin

# Register your models here.
from .models import Question, Answer, Profile, Rating, Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(Tag)