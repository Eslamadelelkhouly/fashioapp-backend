from django.db import models
from django.contrib.auth.models import User
from order.models import Order
# Create your models here.

class Notification(models.Model):
    orderId = models.ForeignKey(Order,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message =  models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True,blank=True)
    isRead = models.BooleanField(default=False)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return "{} | {}".format(self.userid.username, self.userid.id)