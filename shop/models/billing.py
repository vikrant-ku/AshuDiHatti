from django.db import models
from .customer import Customer


class Billing(models.Model):
    user = models.ForeignKey(Customer , on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    country = models.CharField(max_length=20, default='')
    state = models.CharField(max_length=20, default='')
    address1 = models.TextField(default="")
    address2 = models.TextField(default="")
    city = models.CharField(max_length=20, default='')
    zip_code = models.CharField(max_length=10, default='')
    phone = models.CharField(max_length=15, default='')

    def __str__(self):
        return self.name

    @staticmethod
    def get_bill_address_by_id(user_id):
        try:
            return Billing.objects.get(user = user_id)
        except:
            return False
