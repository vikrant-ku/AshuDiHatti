from django.views import  View
from django.shortcuts import render , redirect
from shop.models.customer import Customer
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .signup import Signup
from shop.models.customer import Customer
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from django.contrib import messages
from .home import prod_category, card_len

from django.core.mail import EmailMessage

class Forget_password(View):

    def get(self , request):
        length = card_len(request)  # card len
        category = prod_category(Category, Subcategory)  # header drop down

        cart_prod = {
            'category': category,
            'len': length,
        }
        return render(request , "shop/forget_password.html", cart_prod)

    def post(self, request):

        email = request.POST.get('email')

        customer = Customer.get_customer_by_email(email)



        if customer:

            new_password = Signup.random_password(self, 10)

            customer.password = new_password
            customer.password = make_password(customer.password)
            customer.save()

            email = EmailMessage('New Password', f'Your new password is :"{new_password}" . ', to=[email])
            email.send()

            error_message = "Your password send to your registered email !! "
            messages.success(request, error_message)
            return redirect("home")

        else:
            error_message = "Please check your email and re-enter your registered email !! "
            messages.error(request, error_message)
            return redirect("forget_password")


