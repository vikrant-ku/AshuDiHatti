from django.views import  View
from django.shortcuts import render , redirect
from shop.models.customer import Customer
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from .home import prod_category, card_len
from django.contrib.auth.hashers import  check_password , make_password
from django.contrib import messages


class Change_password(View):

    def get(self , request):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)
        my_product = {
            'category': category,
            'len': len_cart,
        }

        return render(request, 'shop/change_password.html', my_product)

    def post(self, request):

        password = request.POST.get('curr_pass')
        new_password1 = request.POST.get('new_pass1')
        new_password2 = request.POST.get('new_pass2')
        if password != new_password1:
            customer = Customer.get_customer_by_id(request.session.get('customer_id'))

            if  check_password(password, customer.password):

                if new_password1 == new_password2:

                    customer.password = new_password1
                    customer.password = make_password(customer.password)
                    customer.save()

                    error_message = "Your Password Successfully Changed"
                    messages.success(request, error_message)
                    return redirect('profile')
                else:
                    error_message = "Your Password Do not match"
                    messages.error(request, error_message)
                    return redirect('change_password')
            else:
                error_message = "Password do not match please try again"
                messages.error(request, error_message)
                return redirect('change_password')
        else:
            error_message = "Old Password and New Password cannot be same"
            messages.error(request, error_message)
            return redirect('change_password')
