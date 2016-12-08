from django.contrib import admin
from .models import Municipality, Profile, Microsite, Theme, Dataset, Hierarchy, \
    Measure


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country',)
    list_editable = ('country',)

    class Meta:
        model = Dataset


class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'microsite', 'code', 'viz_type', 'height', 'width',)
    list_editable = ('microsite', 'code', 'viz_type', 'height', 'width',)

    class Meta:
        model = Dataset


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'microsite', 'brand_color', 'sidebar_color',
                    'content_color',)
    list_editable = ('microsite', 'brand_color', 'sidebar_color',
                     'content_color',)

    class Meta:
        model = Theme


class MicrositeAdmin(admin.ModelAdmin):
    list_display = ('name', 'municipality', 'selected_theme', 'language',
                    'forum_platform',)
    list_editable = ('municipality', 'selected_theme', 'language',
                     'forum_platform',)
    readonly_fields = ('id', )

    def get_form(self, request, obj=None, **kwargs):
        # Trick to allow filtering the selected_theme drop-down to only show
        # themes that belong to this Microsite
        self.instance = obj
        return super(self.__class__, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Core part of the trick (selected_theme drop-down trick)
        try:
            if db_field.name == 'selected_theme' and self.instance:
                kwargs['queryset'] = \
                    Theme.objects.filter(microsite=self.instance.pk)
        except:
            pass
        return ThemeAdmin(admin_site=self.admin_site, model=Theme)\
            .formfield_for_foreignkey(db_field, request=request, **kwargs)

    class Meta:
        model = Microsite


admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Profile)
admin.site.register(Microsite, MicrositeAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Dataset, DatasetAdmin)
