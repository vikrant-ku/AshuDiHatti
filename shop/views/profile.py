from django.views import  View
from django.shortcuts import render, redirect, get_object_or_404
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.customer import Customer
from shop.models.orders import Orders
from shop.models.billing import Billing

from .home import prod_category, card_len

class Profile(View):

    def get(self , request):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)
        customer = get_object_or_404(Customer, id= int(request.session.get('customer_id')))

        try:
            orders = Orders.objects.filter(customer_id = request.session.get('customer_id')).order_by('-order_date')
        except:
            orders= None

        customer = Customer.objects.get(id = request.session.get('customer_id'))

        #
        billing = Billing.get_bill_address_by_id(request.session.get("customer_id"))
        print(f'billing {billing}')

        cart_prod = {
            'category': category,
            'len': len_cart,
            'orders': orders,
            'customer': customer,
            'billing': billing,
            }
        return render(request , 'shop/profile.html',cart_prod)

def updateProfile(request):
    if request.method == "POST":
        customer = get_object_or_404(Customer, id=int(request.session.get('customer_id')))
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        print(f"name = {name}")
        customer.phone= phone
        customer.customer_name= name
        customer.save()
        request.session['customer_name'] = customer.customer_name

        return redirect('profile')
    else:
        customer = get_object_or_404(Customer, id=int(request.session.get('customer_id')))
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)

        cart_prod = {
            'category': category,
            'len': len_cart,
            'customer': customer,
                     }
        return render(request , 'shop/editprofile.html',cart_prod)

#
class User_billing(View):
    def get(self):
        return redirect('profile')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        country = request.POST.get('country')
        state = request.POST.get('state')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        postal_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        user_address = Billing.get_bill_address_by_id(request.session.get("customer_id"))

        if not user_address:
            billing_address = Billing(user=Customer(request.session.get('customer_id')), name=name, email=email,
                                      country=country, state=state,
                                      address1=address1, address2=address2, city=city, zip_code=postal_code,
                                      phone=phone)
            billing_address.save()
        else:
            user_address.name = name
            user_address.email = email
            user_address.country = country
            user_address.state = state
            user_address.address1 = address1
            user_address.address2 = address2
            user_address.city = city
            user_address.zip_code = postal_code
            user_address.phone = phone
            user_address.save()

        return redirect('profile')
