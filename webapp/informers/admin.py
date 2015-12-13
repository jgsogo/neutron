
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Region, Informer, Interface, Datum


class InformerAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'region',)
    list_filter = ('region',)


class DatumAdmin(admin.ModelAdmin):
    list_display = ('informer', 'interface',)
    list_filter = ('informer__region', 'interface', 'timestamp',)
    search_fields = ('informer__name',)

    def has_add_permission(self, request):
        return False


admin.site.register(Region, MPTTModelAdmin)
admin.site.register(Informer, InformerAdmin)
admin.site.register(Interface)

admin.site.register(Datum, DatumAdmin)
