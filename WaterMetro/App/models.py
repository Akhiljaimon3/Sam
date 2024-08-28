from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    Duedate = models.DateField(blank=True,null=True)
    password = models.CharField(max_length=50)

class Routes(models.Model):
    location = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    departure = models.TimeField()
    Arrival = models.TimeField()
    status = models.IntegerField()
    note = models.TextField(blank=True,null=True)
    
class Route_details(models.Model):
    location = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    travel_time = models.CharField(max_length=20)
    fare = models.IntegerField()

class concession(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    userid = models.FileField()
    plan = models.CharField(max_length=50)
    amount= models.IntegerField()
    status=models.IntegerField()

class concession_history(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    plan = models.CharField(max_length=50)
    amount= models.IntegerField()
    secretcode = models.CharField(max_length=50)
    date = models.DateField()

class booking_history(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    location = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    amount= models.IntegerField()
    secretcode = models.CharField(max_length=50)
    date = models.DateField()
    bookdate = models.DateField()

class PasswordReset(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=4)

class concession_discount(models.Model):
    plan = models.CharField(max_length=50)
    discount_name = models.CharField(max_length=50)
    discount_amount= models.IntegerField()
