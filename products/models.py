from django.db import models
from numpy import product, size

from core.models import TimeStampModel

class Category(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name      = models.CharField(max_length = 100)
    content   = models.CharField(max_length = 255)
    image_url = models.CharField(max_length = 255)
    category  = models.ForeignKey('Category', on_delete = models.PROTECT)

    class Meta:
        db_table = 'sub_categories'

class Product(TimeStampModel):
    name             = models.CharField(max_length = 100)
    is_new           = models.BooleanField()
    is_vegan         = models.BooleanField()
    is_only_online   = models.BooleanField()
    is_made_in_korea = models.BooleanField()
    content          = models.TextField(max_length = 2000, null =True)
    manual           = models.TextField(max_length = 2000, null = True)
    tag              = models.CharField(max_length = 200, null = True)
    sub_category     = models.ForeignKey('SubCategory', on_delete = models.PROTECT)
    image_url_id     = models.ForeignKey('Image_url', on_delete = models.PROTECT)
    component        = models.ManyToManyField('Components', 
                                              through = 'ProductComponent', 
                                              through_fields = ('product_id','component_id'), 
                                              null = True)

    class Meta:
        db_table = 'products'

class ImgaeUrl(models.Model):
    url = models.CharField(max_length = 255)

    class Meta:
        db_table = 'image_urls'

class Component(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        db_table = 'components'

class ProductComponent(models.Model):
    product   = models.ForeignKey('Product', on_delete = models.PROTECT)
    component = models.ForeignKey('Component', on_delete = models.PROTECT)
    important = models.BooleanField()

    class Meta:
        db_table = 'product_component'

class Item(TimeStampModel):
    price     = models.DecimalField(decimal_places = 2)
    stock     = models.IntegerField()
    image_url = models.CharField(max_length = 255)
    product   = models.ForeignKey('Product', on_delete = models.CASCADE)
    size      = models.ForeignKey('Size', on_delete = models.PROTECT)

    class Meta:
        db_table = 'items'
