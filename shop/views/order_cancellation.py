from django.views import  View
from django.shortcuts import render , redirect, get_object_or_404
from shop.models.customer import Customer
from shop.models.orders import Orders
from shop.models.cancle_order import Cancel_order
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.product import Product
from .home import prod_category, card_len
from datetime import datetime
from django.contrib import messages

class Order_cancel(View):
    def get(self, request, **kwargs):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)
        order_id = kwargs['odr_id']
        order= get_object_or_404(Orders,order_id=order_id)


        cart_prod = {
            'category': category,
            'len': len_cart,
            'order':order,
        }

        return render(request, "shop/cancelation.html", cart_prod)

    def post(self, request, **kwargs):
        customer = request.session.get('customer_id')
        order_id = request.POST.get('order_id')
        reason =  request.POST.get('reason')
        order = get_object_or_404(Orders, order_id=int(order_id))
        product = get_object_or_404(Product, id=order.product.id)


        cancel = Cancel_order(customer= Customer(id=int(customer)),
                              order= Orders(order_id=order.order_id), reason=reason)
        cancel.save()
        order.status = "CAN"
        order.order_delevered_date = datetime.now()
        order.register()
        # increase prod stock
        ord_stock = int(order.quantity)
        prod_stock = int(product.stock)
        product.stock = ord_stock+prod_stock
        product.save()


        error_message = 'Order successfully cancelled'
        messages.success(request, error_message)
        return redirect('profile')
