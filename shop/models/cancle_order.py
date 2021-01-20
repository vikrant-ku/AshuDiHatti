from django.db import models
from .customer import Customer
from .orders import Orders



class Cancel_order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    reason = models.CharField(max_length=30)

    def __str__(self):
        return self.customer.customer_name




