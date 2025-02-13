from django.db import models

# Create your models here.

class Item(models.Model):
    """
    Items Model
    """
    category_name = models.CharField(max_length=100)
    que_description = models.CharField(max_length=500,default='default_que')
    que_exp_ans = models.CharField(max_length=1000,default='default_ans')
    exp_ans = models.IntegerField(default=0)
