from django.contrib import admin
from Market.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Painting)
admin.site.register(Sculpture)
admin.site.register(Garment)
admin.site.register(Jewelry)
admin.site.register(GlassArt)
admin.site.register(Cart)
admin.site.register(CartProduct)

