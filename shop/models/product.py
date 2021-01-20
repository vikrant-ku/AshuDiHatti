from django.db import models
from .category import Category
from .sub_category import Subcategory
from django_resized import ResizedImageField


LABEL_CHOICES =(
    ("Sale", "Sale"),
    )

RATING_CHOICES = (
        ('NA', 'New Arrival' ),
        ('BS', 'Best Seller'),
)

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    sr_no = models.SlugField(unique=True)
    subcat_type = models.CharField(max_length=20, null=True, blank=True)
    lable = models.CharField(max_length=15, choices=LABEL_CHOICES, null=True, blank=True)
    color = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    type = models.CharField(max_length=7, choices=RATING_CHOICES, null=True, blank=True)
    description =models.TextField(default="")
    specification =models.TextField(default="")
    rating = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    image1 = ResizedImageField(size=[722, 1024], quality=75, crop=['middle', 'center'], upload_to='uploads/products/')
    image2 = ResizedImageField(size=[722, 1024], quality=75, crop=['middle', 'center'], upload_to='uploads/products/', null=True , blank=True,)
    image3 = ResizedImageField(size=[722, 1024], quality=75, crop=['middle', 'center'], upload_to='uploads/products/', null=True , blank=True,)
    image4 = ResizedImageField(size=[722, 1024], quality=75, crop=['middle', 'center'], upload_to='uploads/products/', null=True , blank=True,)

    def __str__(self):
        return self.sr_no

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)



class FbLive(models.Model):
    prodsr_no = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.prodsr_no.name




