from django.contrib import admin
from stock.models import *

admin.site.register(Categories)
admin.site.register(Transactions)
admin.site.register(Products)
admin.site.register(Suppliers)
admin.site.register(Entries)
admin.site.register(Exits)