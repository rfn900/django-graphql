from django.contrib import admin
from .models import Stock, Portfolio, Trade

# Register your models here.
admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Trade)
