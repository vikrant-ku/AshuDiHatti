from rest_framework import serializers
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.customer import Customer, Cart
from shop.models.contact_us import Contact
from shop.models.product import Product, FbLive
from shop.models.orders import Orders
# from shop.models.payment import Payment
from shop.models.billing import Billing
from shop.models.cancle_order import Cancel_order
from shop.models.subscribers import Subscriber
from django.contrib.auth.hashers import make_password

class Category_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class Sub_Ctegory_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class Customer_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('url','customer_name', 'phone', 'email', 'password')
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Customer.objects.create(
               customer_name=validated_data['customer_name'],
                email=validated_data['email'],
                phone=validated_data['phone'],
                password=validated_data['password']
                  )
        user.password = make_password(user.password)
        user.save()
        return user


class Contact_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class Product_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class Oreder_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class Cart_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class Billing_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'

class Cancel_order_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cancel_order
        fields = '__all__'

class Subscriber_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class FacebookLive_serilizer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FbLive
        fields = '__all__'

# class Payment_serilizer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'

class EmailVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    class Meta:
        model = Customer
        fields = ['email']

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6)
    class Meta:
        model = Customer
        fields = ['email', 'password']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    oldpassword = serializers.CharField(max_length=68, min_length=6)
    newpassword = serializers.CharField(max_length=68, min_length=6)

    class Meta:
        model = Customer
        fields = ['email','oldpassword', 'newpassword']

class UserResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    class Meta:
        model = Customer
        fields = ['email']












