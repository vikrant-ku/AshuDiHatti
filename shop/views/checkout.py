from django.views import  View
from django.shortcuts import render , redirect, reverse
from shop.models.orders import Orders
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.product import Product
from shop.models.customer import Customer
# from cart.models.payment import Payment
from django.contrib import messages
from django.conf import settings
from shop.models.customer import  Cart
from shop.models.billing import  Billing
from .login import load_cart_DB_to_session
from .home import prod_category, card_len
from django.views.decorators.csrf import csrf_exempt
from shop.paytm import Checksum
MERCHANT_KEY = 'CIVmkqDJzoGScmoX'

class Checkout(View):

    def get(self , request):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)
        cart = load_cart_DB_to_session(int(request.session['customer_id']))
        request.session['cart'] = cart


        cart_prod = {}
        try:
            cart = request.session.get('cart')
        except:
            cart = None
        if cart != None:
            product = []
            for id, value in cart.items():
                product.append(id)
                product.append(value)
            ids = list(request.session.get('cart').keys())
            if ids:

                products = Product.get_products_by_id(ids)
                #
                user_address = Billing.get_bill_address_by_id(request.session.get("customer_id"))


                cart_prod = {
                 'category': category,
                'len': len_cart,
                'prod':products,
                'user_address': user_address,
                            }
                return render(request, 'shop/checkout.html', cart_prod)
        messages.error(request, "Your cart is Empty")
        return redirect('home')
#
#
#
    def post(self , request):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)

        cart = request.session.get('cart')
        product = []
        for id, value in cart.items():
            product.append(id)
            product.append(value)
        ids = list(request.session.get('cart').keys())
        if ids:
            products = Product.get_products_by_id(ids)

        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        phone = request.POST.get('phone')
        totalprice = int(request.POST.get('total_price'))

        user_address = Billing.get_bill_address_by_id(request.session.get("customer_id"))

        # save user billing address
        if not user_address:
            billing_address = Billing(user = Customer(request.session.get('customer_id')),name=name, email=email, country=country, state=state,
                               address1=address1, address2=address2, city=city, zip_code=postal_code, phone=phone)
            billing_address.save()

        param = {'name': name, 'email': email, 'country': country, 'state': state, 'address': address1 + " " + address2,
                 'city': city, 'postal_code': postal_code,'phone': phone, 'total_price': totalprice}


        products = Product.get_products_by_id(list(cart.keys()))
        order_id =""
        for product in products:
            order = Orders(
                                customer =Customer(id=request.session.get('customer_id')),
                                product= product,color =cart.get(str(product.id))[1], quantity=cart.get(str(product.id))[0],
                                price=get_price(product,cart.get(str(product.id))[0]),
                                name=name, email=email, country=country, state=state,
                                address=address1+" "+address2, city=city, zip_code=postal_code,
                                phone=phone)
            order.save()
            order_id += str(order.order_id)

        param_dict = {

            'MID': 'lieNmi15357207091028',
            'ORDER_ID': 'ODR-31',
            'TXN_AMOUNT': '100.00',
            'CUST_ID': name,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://ashudihatti.in/handlerequest/',

            }
        chucksum = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

        param_dict['CHECKSUMHASH']= chucksum
        return render(request, 'shop/payment.html', {'param_dict': param_dict})

#
#         #  update product stock
#             product.stock -= int(cart.get(str(product.id))[0])
#             product.save()
#        #
#        # # empty cart
#        #  request.session.pop('cart')
#        #
#        #  user = Cart.objects.get(user=int(request.session.get('customer_id')))
#        #  user.cart = ''
#        #  user.save()
#        #
#        #  cart_prod = {
#        #      'category': category,
#        #      'len': len_cart,
#        #      'prod': products
#        #      # 'user_address': user_address,
#        #  }
#        #  return redirect('profile')
#        #
#        #      payment = Payment(user= Customer(id=request.session.get('customer_id')),
#        #                        order= order_id,
#        #                        txn_id= txn_id,
#        #                        payer_id= payer_id,
#        #                        amount= totalprice)
#        #      payment.save()
#
#             # empty cart
#         request.session.pop('cart')
#         try:
#             user = Cart.get_cart_by_user_id(user_id=request.session.get('customer_id'))
#             if user:
#                 user.cart = ''
#         except:
#             pass
#
#
#         return render(request, 'shop/payment_success.html',{ 'len': len_cart})
# #         else:
# #             return render(request, 'payment_cancelled.html',{ 'len': len_cart})


def get_price(product, quantity):
    if product.discount_price > 0:
        return int(product.discount_price)*int(quantity)
    else:
        return int(product.price)*int(quantity)

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    print(f"form ={form}")
    try:
        response_dict = {}
        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]

        verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
        if verify:
            if response_dict['RESPCODE'] == '01':
                print('order successful')
            else:
                print('order was not successful because' + response_dict['RESPMSG'])
        return render(request, 'shop/paymentstatus.html', {'response': response_dict})

    except:
        return render(request, 'shop/404.html')





# def payment(request, status=None):
#     len_cart = card_len(request)
#     if status == 'UGF5bWVudEZhaWw=':
#         return render(request, 'payment_cancelled.html',{ 'len': len_cart})

