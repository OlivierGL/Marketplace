from django.contrib import admin

from Market.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
