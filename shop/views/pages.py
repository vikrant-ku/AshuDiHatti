from django.shortcuts import render , redirect , HttpResponseRedirect
from django.views import View
from django.contrib import messages
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.subscribers import Subscriber
from .home import prod_category, card_len
from shop.models.contact_us import Contact


class About_us(View):
    def get(self, request):
        length = card_len(request)
        category = prod_category(Category, Subcategory)
        cart_prod = {
            'category': category,
            'len': length,
        }
        return render(request, 'shop/contact_us.html', cart_prod)

class FAQ(View):
    def get(self, request):
        length = card_len(request)
        category = prod_category(Category, Subcategory)
        cart_prod = {
            'category': category,
            'len': length
        }
        return render(request, 'shop/faqs.html', cart_prod )

class Terms(View):
    def get(self, request):
        length = card_len(request)
        category = prod_category(Category, Subcategory)
        cart_prod = {
            'category': category,
            'len': length
        }
        return render(request, 'terms_condition.html', cart_prod )

class Contact_us(View):
    def get(self, request):
        length = card_len(request)
        category = prod_category(Category, Subcategory)
        cart_prod = {
            'category': category,
            'len': length
        }
        return render(request, 'shop/contact_us.html', cart_prod )
#
    def post(self, request):
        Message = ''
        print(f"request {request.POST}")
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('number')
        message = request.POST.get('message')

        contact = Contact(name=name, email=email, phone=phone, message=message)
        contact.save()
        Message = "Your Message Has been send. We will Get back to you soon..."
        messages.success(request, Message)
        return redirect('contact')

class Subscribers(View):
    def post(self, request):

        email = request.POST.get('subscribe-email')
        try:
            subscr = Subscriber.objects.get(email=email)
        except:
            subscr= None
        if subscr== None:
            subscriber = Subscriber(email=email)
            subscriber.save()
            return redirect('home')
        else:
            Message = "Your are already Subscribed."
            messages.error(request, Message)
            return redirect('home')


class Support(View):
    def get(self, request):
        length = card_len(request)
        category = prod_category(Category, Subcategory)

        cart_prod = {
            'category': category,
            'len': length
        }
        return render(request, 'shop/payment_failure.html', cart_prod)


