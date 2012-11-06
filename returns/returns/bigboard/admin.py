from django.contrib import admin
from returns.bigboard.models import Slice, Race, Result

class SliceAdmin(admin.ModelAdmin):
    pass

class RaceAdmin(admin.ModelAdmin):
    pass

class ResultAdmin(admin.ModelAdmin):
    pass

admin.site.register(Slice, SliceAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(Result, ResultAdmin)
