from django.contrib import admin
from .models import CarMake, CarModel, CarDealer, DealerReview

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['carModels', 'name', 'dealerID', 'carType', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    fields = ['name', 'description']

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
