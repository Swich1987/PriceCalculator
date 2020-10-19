from django.contrib import admin
from api.models import State, StateTax, Discount

# Register your models here.

admin.site.register(State)
admin.site.register(StateTax)
admin.site.register(Discount)
