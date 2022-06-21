from django.db import models

from core.time_stamp_modules import TimeStampModel

class User(TimeStampModel):
    username     = models.CharField(max_length = 50, unique = True)
    password     = models.CharField(max_length = 300)
    email        = models.CharField(max_length = 100, unique = True)
    phone_number = models.CharField(max_length = 50, unique = True)
    adress       = models.CharField(max_length = 200, null = True)
    first_name   = models.CharField(max_length = 50)
    last_name    = models.CharField(max_length = 50)
    nick_name    = models.CharField(max_length = 50, unique = True, null = True)

    class Meta:
        db_table = 'users'
