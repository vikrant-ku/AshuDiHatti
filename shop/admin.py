from django.contrib import admin
from .models.category import Category
from .models.product import Product, FbLive
from .models.sub_category import Subcategory

from .models.customer import Customer, Cart
from .models.orders import Orders
from .models.contact_us import Contact
from .models.subscribers import Subscriber
from .models.billing import Billing
from .models.cancle_order import Cancel_order
# from .models.replace import Replace
# from .models.payment import Payment
#
#
# # Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class SubcatAdmin(admin.ModelAdmin):
    list_display = ( 'name','category')
    list_filter = ('name','category', )
    search_fields = ('name','category__name',)
    prepopulated_fields = {'slug': ('name',)}

class ProdAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory','subcat_type', 'lable', 'type')
    list_filter = ('category', 'subcategory','subcat_type', 'type', 'lable')
    search_fields = ('name','category__name', 'subcategory__name', 'sr_no', 'subcat_type', 'type','lable')
    list_editable = ('lable', 'type')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'order_date', 'status', 'order_delevered_date')
    search_fields = ['name', 'email',  'status']
    list_editable = ( 'status',)

class CancelAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'reason')

class FBLiveAdmin(admin.ModelAdmin):
    raw_id_fields = ("prodsr_no",)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcatAdmin)
admin.site.register(Product, ProdAdmin)
admin.site.register(FbLive, FBLiveAdmin)
admin.site.register(Customer)
admin.site.register(Orders, OrderAdmin)
admin.site.register(Cart)
# admin.site.register(Payment)
admin.site.register(Subscriber)
admin.site.register(Cancel_order, CancelAdmin)
admin.site.register(Billing)
admin.site.register(Contact, ContactAdmin)

