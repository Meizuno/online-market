from django.db import models


class User(models.Model):
    image = models.ImageField("Foto", null=True, blank=True, upload_to='user_images')
    firstName = models.CharField("First name", max_length=20)
    lastName = models.CharField("Last name", max_length=20)
    email = models.EmailField("Email")
    # phone = models.IntegerField("Phone", blank=True, null=True)
    city = models.CharField("City", max_length=20, blank=True)
    address = models.CharField("Address", max_length=20, blank=True)
    password = models.TextField("Password")
    status = models.CharField(max_length=20, default="registered")


class Crop(models.Model):
    image = models.ImageField("Foto", null=True, blank=True, upload_to='crop_images')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField("First name", max_length=20)
    kind = models.CharField("Kind", max_length=20)
    amount = models.CharField("Amount", max_length=20)
    price = models.FloatField("Price", default=0)
    status = models.BooleanField("Status", default=False)
    editing = models.BooleanField("Status", default=False)


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    description = models.TextField("Description", null=True)
