from django.contrib import admin
from .models import Municipality, Profile, Microsite, Theme, Dataset, Hierarchy, \
    Measure

admin.site.register(Municipality)
admin.site.register(Profile)
admin.site.register(Microsite)
admin.site.register(Theme)
admin.site.register(Measure)
admin.site.register(Hierarchy)
admin.site.register(Dataset)
