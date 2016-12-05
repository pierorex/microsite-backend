from django.contrib import admin
from .models import Municipality, Profile, Microsite, Theme, Dataset, Hierarchy, \
    Measure


class ThemeAdmin(admin.ModelAdmin):
    class Meta:
        model = Theme


class MicrositeAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.instance = obj
        return super(self.__class__, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'selected_theme' and self.instance:
            kwargs['queryset'] = \
                Theme.objects.filter(microsite=self.instance.pk)
        return ThemeAdmin(admin_site=self.admin_site, model=Theme)\
            .formfield_for_foreignkey(db_field, request=request, **kwargs)

    class Meta:
        model = Microsite


admin.site.register(Municipality)
admin.site.register(Profile)
admin.site.register(Microsite, MicrositeAdmin)
admin.site.register(Theme)
admin.site.register(Measure)
admin.site.register(Hierarchy)
admin.site.register(Dataset)
