from django.shortcuts import render , redirect, get_object_or_404
from django.views import  View
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from .home import prod_category , card_len
from shop.models.orders import Orders
from datetime import datetime, timedelta


class Order_tarck(View):
    def get(self , request, **kwargs):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)

        try:
            user= request.session['customer_id']
        except:
            user = None
        if user!= None:
            order_id = kwargs['odr_id']
            order = get_object_or_404(Orders, order_id=order_id )

            order_date = order.order_date.replace(tzinfo=None)+ timedelta(hours=24)
            today = datetime.now()
            flag = order_date > today

            cart_prod = {
                'category': category,
                'len': len_cart,
                'order':order,
                'flag':flag,
            }
            return render(request, 'shop/order_tracking.html', cart_prod)
        else:
            return redirect('home')