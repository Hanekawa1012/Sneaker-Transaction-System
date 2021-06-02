from django.contrib import admin
from .models import buyer,seller,sneaker,inventory,order,sold,customization


# Register your models here.
admin.site.register(buyer)
admin.site.register(seller)
admin.site.register(sneaker)
admin.site.register(inventory)
admin.site.register(order)
admin.site.register(sold)
admin.site.register(customization)