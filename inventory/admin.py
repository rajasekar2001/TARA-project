from django.contrib import admin
from .models import RawMaterial,FinishedProduct,Production

admin.site.register(RawMaterial)
admin.site.register(Production)
admin.site.register(FinishedProduct)

