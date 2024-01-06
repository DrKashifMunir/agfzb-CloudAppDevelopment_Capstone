from django.db import models
from django.utils.timezone import now

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='Honda')
    description = models.CharField(null=False, max_length=30)
    def __str__(self):
        return self.name + " " + self.description

class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    carModels = models.ForeignKey('CarMake', null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='Civic')
    dealerID = models.IntegerField()
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    carType = models.CharField(null=True, max_length=20)
    year = models.DateField(null=True)
    def __str__(self):
        return self.name + " " + str(self.dealerID)  + " " + self.carType + " " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, _id, _rev, id, city, state, st, address, zip, lat, lng, short_name, full_name):
        self._id = _id
        self._rev = _rev
        self.id = id 
        self.city = city
        self.state = state
        self.st = st
        self.address = address 
        self.zip = zip
        self.lat = lat
        self.long = lng
        self.short_name = short_name 
        self.full_name = full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, _id, _rev, id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year):
        self._id = _id
        self._rev = _rev
        self.id = id
        self.name = name
        self.dealership = dealership
        self.review = review
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
