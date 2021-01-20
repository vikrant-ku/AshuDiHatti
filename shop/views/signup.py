from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password , check_password
from django.views import View
from django.http import HttpResponseRedirect
from shop.models.customer import Customer
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from django.contrib import messages
from django.core.mail import EmailMessage
# from .pages import
from .home import prod_category, card_len
import string
import random
#
#
class Signup(View):
    def get(self, request):
        length = card_len(request)  # card len
        category = prod_category(Category, Subcategory)  # header drop down

        cart_prod = {
            'category': category,
            'len': length,
        }

        return render(request, 'shop/signup.html', cart_prod)
#
    def post(self, request):
        length = card_len(request)  # card len
        category = prod_category(Category, Subcategory)  # header drop down

        postData = request.POST
        customer_name = postData.get('name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        password1 = postData.get('confirmpassword')
        error_message = None

        customer = {'name':customer_name,
                            'phone':phone,
                            'email':email,
                            'password':password,
                            'confirmpassword': password1}

        error_message = self.validateCustomer(customer)

        if not error_message:
            otp = Signup.random_password(self, 6)
            email = EmailMessage('OTP', f'Your One Time Password is :"{otp}" . ', to=[email])
            email.send()
            customer['otp'] = otp
            return render(request, 'shop/email_verification.html',  {'customer': customer, 'category': category, 'len': length,})
        else:
            messages.error(request, error_message)
            return redirect('signup')

    def validateCustomer(self, customer):
        error_message = None
        if not customer['name']:
            error_message = "Name  Required !!"
        elif len(customer['name']) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer['phone']:
            error_message = 'Phone Number required'
        elif len(customer['phone']) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif customer['password'] != customer['confirmpassword']:
            error_message = 'Password do not match'
        elif len(customer['password']) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer['email']) < 5:
            error_message = 'Email must be 5 char long'
        elif Customer.isExists(customer['email']):
            error_message = 'Email Address Already Registered..'
        return error_message

    def random_password(self, n):

        LETTERS = string.ascii_letters
        NUMBERS = string.digits
        PUNCTUATION = '@#$&'

        printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'
        printable = list(printable)
        random.shuffle(printable)
        random_password = random.choices(printable, k=n)
        random_password = ''.join(random_password)

        return random_password


def validate_email(request):
    if request.method == 'POST':
        length = card_len(request)  # card len
        category = prod_category(Category, Subcategory)  # header drop down

        postData = request.POST
        customer_name = postData.get('name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        otp = postData.get('otp')
        user_otp = postData.get('user_otp')
        if otp == user_otp:
            customer = Customer(customer_name=customer_name, phone=phone, email=email,password=password)
            customer.password = make_password(customer.password)
            customer.save()
            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.customer_name
            return redirect('home')
        else:

            customer = {'name': customer_name,
                        'phone': phone,
                        'email': email,
                        'password': password,
                        'otp': otp }
            error_message = "Invalid OTP"
            messages.error(request, error_message)
            return render(request, 'shop/email_verification.html',
                          {'customer': customer, 'category': category, 'len': length, })



    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
