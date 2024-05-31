from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    catname = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.catname


class Subcategory(models.Model):
    subcatname = models.CharField(max_length=255,null=True)
    image = models.ImageField(upload_to='SubCategoryImages/',null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcategory_set')
    date = models.DateField(auto_now=True,null=True)
    time = models.TimeField(auto_now=True,null=True)

    def __str__(self):
        return self.subcatname

class Product(models.Model):
    productname = models.CharField(max_length=255,null=True)
    pimage_thumbnail = models.ImageField(upload_to='ProductImages/',null=True)
    price = models.FloatField(null=True)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    description = RichTextField(config_name='default',null=True)
    specification = RichTextField(config_name='default',null=True)
    date = models.DateField(auto_now=True,null=True)
    time = models.TimeField(auto_now=True,null=True)


    def __str__(self):
        return self.productname

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    images = models.ImageField(upload_to='ProductImages/',null=True)

    def __str__(self):
        return self.product.productname

class CustomerProfile(models.Model):
    GENDER_CHOICES = [
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profileName = models.CharField(max_length=255,null=True)
    profileImage = models.ImageField(upload_to='CustomerProfileImages/',null=True)
    bio = models.TextField(null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES,null=True)
    country = models.CharField(max_length=255,null=True)
    address = models.CharField(max_length=255,null=True)
    phone = models.CharField(max_length=255,null=True)
    datetimep = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.user.username
    
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cdatetime = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.product.productname
       
class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wdatetime = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.product.productname


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255,null=True)
    phone = models.BigIntegerField(null=True)
    street = models.CharField(max_length=255,null=True)
    landmark = models.CharField(max_length=255,null=True)
    city = models.CharField(max_length=255,null=True)
    state = models.CharField(max_length=255,null=True)
    pincode = models.IntegerField(null=True)
    country = models.CharField(max_length=255,null=True)
    alt_phone = models.BigIntegerField(null=True, blank=True)



class Order(models.Model):

    STATUS =(
        ('Pending','Pending'),
        ('Order Confirmed','Order Confirmed'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )

    order_id = models.CharField(max_length=100,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    odatetime = models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=50,null=True,choices=STATUS)

    
    def __str__(self):
        return  f"Order ID: {self.order_id} - User: {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order: {self.order.order_id} - Product: {self.product.productname} - Quantity: {self.quantity}"