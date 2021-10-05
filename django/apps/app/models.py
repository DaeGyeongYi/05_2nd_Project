# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.db import models
from django.db import models
from django.contrib.auth.models import User
class Region :
    region_text = models.CharField(max_length=50)
    region_num =models.IntegerField(default=0)

class HighSchool :
    high_name = models.CharField(max_length=50)
    snu_su = models.IntegerField(default=0)
# Create your models here.

