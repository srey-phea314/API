from django.contrib import admin
from .models import *
from .models import AccessToken
admin.site.register(HeroSection)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(SmallBanner)
admin.site.register(Blog)
admin.site.register(QRCode)
admin.site.register(ProductImage)
admin.site.register(SizeOption)
admin.site.register(Customer)
@admin.register(AccessToken)
class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('token',)