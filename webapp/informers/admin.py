from django.contrib import admin

from .models import Region, Informer, LocalizedInformer, Interface, Datum


admin.site.register(Region)
admin.site.register(Informer)
admin.site.register(LocalizedInformer)
admin.site.register(Interface)

admin.site.register(Datum)
