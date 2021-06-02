
from django.db import models

# Create your models here.
class buyer (models.Model):
    username = models.CharField(max_length=25,unique=True)
    password  = models.CharField(max_length=30)
    address= models.CharField(max_length=100)
    c_time=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.username
    class Meta:
        ordering=['c_time']
class seller (models.Model):
    username = models.CharField(max_length=25,unique=True)
    password  = models.CharField(max_length=30)
    address= models.CharField(max_length=100)
    c_time=models.DateField(auto_now_add=True)
    def __str__(self):
        return self.username
    class Meta:
        ordering=['c_time']
class sneaker(models.Model):
    name=models.CharField(max_length=100,unique=True)
    price=models.CharField(max_length=30)
    brand = models.CharField(max_length=40)
    img=models.ImageField(upload_to='img')
class inventory(models.Model):
    sneakerid = models.ForeignKey(sneaker,on_delete=models.DO_NOTHING)
    seller= models.ForeignKey(seller,to_field='username',on_delete=models.DO_NOTHING)
class sold(models.Model):
    soldid = models.IntegerField(primary_key=True,unique=True)
    sneakerid = models.ForeignKey(sneaker,on_delete=models.DO_NOTHING)
class customization(models.Model):
    color = models.CharField(max_length=10,null=True)
class order(models.Model):
    inventoryid = models.ForeignKey(sold,on_delete=models.DO_NOTHING,null=True)
    buyer=models.ForeignKey(buyer,to_field='username',on_delete=models.DO_NOTHING,related_name='buyer')
    seller = models.ForeignKey(seller,to_field='username',on_delete=models.DO_NOTHING,related_name='seller')
    custom=models.ForeignKey(customization,to_field='id',on_delete=models.DO_NOTHING,null=True)
    c_time = models.DateField(auto_now_add=True)
    class Meta:
        ordering=['c_time']





# Create your models here.
# Change your models (in models.py).
# Run python manage.py migrate to apply those changes to the database.
# Run python manage.py makemigrations to create migrations for those changes.


