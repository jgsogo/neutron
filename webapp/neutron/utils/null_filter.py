# -*- coding: utf-8 -*-

from django.contrib.admin import SimpleListFilter


class NullListFilter(SimpleListFilter):

    def lookups(self, request, model_admin):
        return (
            ('1', 'Null', ),
            ('0', '!= Null', ),
        )

    def queryset(self, request, queryset):
        if self.value() in ('0', '1'):
            kwargs = { '{0}__isnull'.format(self.parameter_name): self.value() == '1'}
            return queryset.filter(**kwargs)
        return queryset


def null_filter(field, title_=None, values_=None):
    class NullListFieldFilter(NullListFilter):
        parameter_name = field
        title = title_ or parameter_name

        def lookups(self, request, model_admin):
            if values_:
                return ((key, value) for key, value in values_.items())
            else:
                return super(NullListFieldFilter, self).lookups(request, model_admin)

    return NullListFieldFilter