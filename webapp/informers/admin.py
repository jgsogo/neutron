from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Region, Informer, LocalizedInformer, Interface, Datum

class LocalizedInformerAdmin(admin.ModelAdmin):
    list_display = ('informer', 'region',)
    list_filter = ('region',)


class RegionInline(admin.TabularInline):
    extra = 0
    model = LocalizedInformer


class InformerAdmin(admin.ModelAdmin):
    inlines = [RegionInline,]


class DatumAdmin(admin.ModelAdmin):
    list_display = ('informer', 'interface',)
    list_filter = ('informer__region', 'interface', 'timestamp',)
    search_fields = ('informer__name',)

    def has_add_permission(self, request):
        return False


admin.site.register(Region, MPTTModelAdmin)
admin.site.register(Informer, InformerAdmin)
admin.site.register(LocalizedInformer, LocalizedInformerAdmin)
admin.site.register(Interface)

admin.site.register(Datum, DatumAdmin)
