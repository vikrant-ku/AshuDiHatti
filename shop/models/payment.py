# from django.db import models
# from datetime import datetime
# from .customer import Customer
#
# class Payment (models.Model):
#     user = models.ForeignKey(Customer , on_delete=models.CASCADE)
#     order = models.CharField(max_length=50, default="")
#     txn_id = models.CharField(max_length=50, default="")
#     payer_id = models.CharField(max_length=50, default="")
#     mode = models.CharField(max_length=20, default="")
#     amount = models.IntegerField(default=0)
#     date = models.DateTimeField(default=datetime.now)
#
#     def __str__(self):
#         return self.user.customer_name