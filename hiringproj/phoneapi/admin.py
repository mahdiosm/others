from django.contrib import admin
from .models import Phone


class PhoneAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "price", "color", "screen_size", "is_available", "creator_country")
    search_fields = ("brand", "model", "color", "creator_country")


admin.site.register(Phone, PhoneAdmin)
