import uuid

from django.db import models

from users.models       import User
from products.models    import Item
from core.models        import TimeStampModel

class Cart(models.Model):
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    item     = models.ForeignKey('products.Item', on_delete = models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'carts'

class OrderItem(models.Model):
    user     = models.ForeignKey('users.User', on_delete = models.CASCADE)
    item     = models.ForeignKey('products.Item', on_delete = models.CASCADE)
    quantity = models.IntegerField()
    order    = models.ForeignKey('Order', on_delete = models.CASCADE)

    class Meta:
        db_table = 'order_items'

class OrderStatus(models.Model):
    status = models.CharField(max_length = 100)

    class Meta:
        db_table = 'order_statuses'

class Customer(TimeStampModel):
    first_name   = models.CharField(max_length = 50)
    last_name    = models.CharField(max_length = 50)
    phone_number = models.CharField(max_length = 50)
    email        = models.CharField(max_length = 100)
    adress       = models.CharField(max_length = 200)

    class Meta:
        db_table = 'customers'

class Order(TimeStampModel):
    order_number = models.UUIDField(default = uuid.uuid4)
    message      = models.CharField()
    customer     = models.ForeignKey('Customer', on_delete = models.SET_NULL, null = True)
    status       = models.ForeignKey('Status', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'orders'