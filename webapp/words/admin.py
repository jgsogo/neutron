from django.contrib import admin

from .models import Definition, Dictionary, Context, CoarseWord, WordUse


admin.site.register(Definition)
admin.site.register(Dictionary)
admin.site.register(Context)

admin.site.register(CoarseWord)
admin.site.register(WordUse)
