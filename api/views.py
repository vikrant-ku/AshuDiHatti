from rest_framework import viewsets
import json
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import Category_serilizer, Customer_serilizer, Contact_serilizer, Product_serilizer , Oreder_serilizer, UserLoginSerializer
from .serializers import Cart_serilizer, Billing_serilizer, Cancel_order_serilizer, Subscriber_serilizer, EmailVerificationSerializer, Sub_Ctegory_serilizer
from .serializers import UserChangePasswordSerializer, UserResetPasswordSerializer, FacebookLive_serilizer #, Payment_serilizer,
from shop.models.category import Category
from shop.models.sub_category import Subcategory
# from shop.models.payment import Payment
from shop.models.customer import Customer, Cart
from shop.models.contact_us import Contact
from shop.models.product import Product,  FbLive
from shop.models.orders import Orders
from shop.models.billing import Billing
from shop.models.cancle_order import Cancel_order
from shop.models.subscribers import Subscriber
from shop.views.signup import Signup
from django.core.mail import EmailMessage
from django.http import JsonResponse

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = Category_serilizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name' , 'slug']
    http_method_names = ['get']

class Sub_CategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = Sub_Ctegory_serilizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'slug' ]
    http_method_names = ['get']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = Customer_serilizer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = Contact_serilizer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = Product_serilizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'subcategory', 'subcat_type', 'type']
    http_method_names = ['get']


class FacebookLiveViewSet(viewsets.ModelViewSet):
    queryset =FbLive.objects.all()
    serializer_class = FacebookLive_serilizer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date']
    http_method_names = ['get']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = Oreder_serilizer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = Cart_serilizer


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = Billing_serilizer


class Cancel_orderViewSet(viewsets.ModelViewSet):
    queryset = Cancel_order.objects.all()
    serializer_class = Cancel_order_serilizer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = Subscriber_serilizer

# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = Payment_serilizer

class VerifyEmail(viewsets.ViewSet):
    serializer_class = EmailVerificationSerializer
    http_method_names = ['get','post']
    data = {}
    def get_queryset(self):
        return JsonResponse(self.data)

    def create(self, request):
        email = request.data['email']
        try:
            user = Customer.objects.get(email=email)
        except:
            user = None
        if user != None:
            self.data['error']='email is already exist.'
            return JsonResponse(self.data)
        else:
            otp = Signup.random_password(self, 6)
            email = EmailMessage('OTP', f'Your One Time Password is :"{otp}" . ', to=[email])
            email.send()
            self.data['error']=otp
            return JsonResponse(self.data)


class UserLogin(viewsets.ViewSet):
    serializer_class = UserLoginSerializer
    http_method_names = ['get', 'post']
    data = {}
    def get_queryset(self):
        return JsonResponse(self.data)

    def create(self, request):

        email = request.data['email']
        password = request.data['password']
        try:
            user = Customer.objects.get(email=email)
        except:
            user = None
        if user != None:
            flag = check_password(password, user.password)
            if flag:
                self.data["id"] = user.id
                self.data["name"] = user.customer_name
                self.data["phone"] = user.phone
                self.data["email"] = user.email
                return JsonResponse(self.data)
            return JsonResponse({'error': 'Password Do not Match'})
        else:
            return JsonResponse({'error': 'User is not Exist '})


class UserChangePassword(viewsets.ViewSet):
    serializer_class = UserChangePasswordSerializer
    http_method_names = ['get', 'post']
    data = {}
    def get_queryset(self):
        return JsonResponse(self.data)

    def create(self, request):
        email = request.data['email']
        old = request.data['oldpassword']
        new = request.data['newpassword']
        try:
            user = Customer.objects.get(email=email)
        except:
            user = None
        if user != None:
            flag = check_password(old, user.password)
            if flag:
                user.password = new
                user.password = make_password(user.password)
                user.save()
                self.data['user']="Password Successfully Changed"
                return JsonResponse(self.data)
            self.data['user']="Password Do not Match"
            return JsonResponse(self.data)
        else:
            self.data['user']="Email is not valid"
            return JsonResponse(self.data)


class UserResetPassword(viewsets.ViewSet):
    serializer_class = UserResetPasswordSerializer
    data = {}
    def get_queryset(self):
        return JsonResponse(self.data)
    def create(self, request):
        email = request.data['email']
        try:
            user = Customer.objects.get(email=email)
        except:
            user = None
        if user != None:
            newpass = Signup.random_password(self, 10)
            user.password = newpass
            user.password = make_password(user.password)
            user.save()
            email = EmailMessage('OTP', f'Your New Password is :"{newpass}" . ', to=[email])
            email.send()
            self.data["user"]="success"
            return JsonResponse(self.data)
        else:
            self.data["user"] = "Email is not valid"
            return JsonResponse(self.data)


class Subcat_type(APIView):
    def get(self,request):

        cat = request.GET.get('category')
        subcat= request.GET.get('subcategory')

        if cat != None and subcat !=None:
            prod = Product.objects.filter(category=int(cat), subcategory=int(subcat)).values_list('subcat_type', flat=True).distinct()
            data = {}
            items = []
            for item in prod:
                items.append(item)
            data[subcat] = items
            return HttpResponse(json.dumps(data), content_type="application/json")
        elif cat != None:
            prod = Product.objects.filter(category=int(cat)).values_list('subcat_type',flat=True).distinct()
            data = {}
            items = []
            for item in prod:
                items.append(item)
            data[cat]=items
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            response_data = {'data': None}
            return HttpResponse(json.dumps(response_data), content_type="application/json")








