from django.urls import path
from .views.home import Index
from .views.pages import About_us, FAQ, Contact_us, Terms, Subscribers, Support
from .views.shop import Fbshop, Shop
from .views.signup import Signup, validate_email
from .views.login import  Login, logout
from .views.product_detail import Product_detail
from .views.profile import Profile,updateProfile, User_billing
from .views.cart import Cart, delete_item, update_item
from .views.checkout import Checkout, handlerequest
from .views.changepassword import Change_password
from .views.order_tracking import Order_tarck
from .views.search import Search
from .views.forgetpassword import Forget_password
from .views.order_cancellation import Order_cancel
from .middlewares.auth import auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('about_us/', About_us.as_view(), name='about'),
    path('subscriber/', Subscribers.as_view(), name='subscribers'),
    path('contact_us/', Contact_us.as_view(), name='contact'),
    path('faqs/', FAQ.as_view(), name='faqs'),
    path('terms/', Terms.as_view(), name='terms'),
    path('support/', Support.as_view(), name='terms'),
    path('subscriber/', Subscribers.as_view(), name='subscribers'),


    path('facebookLive/', Fbshop.as_view()),
    path('facebookLive/<str:date>/', Fbshop.as_view()),

    path('shop/<str:category>/', Shop.as_view(), name='shop'),
    path('shop/<str:category>/<str:subcat>/', Shop.as_view(), name='shop'),
    path('shop/<str:category>/<str:subcat>/<str:subcat_type>/', Shop.as_view(), name='shop'),


    path('search/', Search.as_view(), name='search'),

    path('product_detail/<str:name>/<str:slug>/', Product_detail.as_view(), name='product_detail'),

    path('cart/', auth_middleware(Cart.as_view()), name='cart'),
    path('cart/<int:id>/', delete_item, name='delete_item'),
    path('cart/update_item/', auth_middleware(update_item), name='update_item'),
    path('cart/checkout/', auth_middleware(Checkout.as_view()), name='checkout'),

    path("handlerequest/", handlerequest, name="HandleRequest"),

    path('profile/', auth_middleware(Profile.as_view()), name='profile'),
    path('profile/update_profile/', auth_middleware(updateProfile), name='update_profile'),

    path('profile/billing_shipping/', User_billing.as_view(), name='profile-billing'),
    path('profile/order/<str:name>/<int:odr_id>/', Order_tarck.as_view()),
    path('profile/order/order_cancellation/<str:name>/<int:odr_id>/', Order_cancel.as_view()),
    path('profile/change_password/', Change_password.as_view(), name='change_password'),

    path('signup/', Signup.as_view(), name='signup'),
    path('signup/validate/', validate_email, name='validate_email'),
    path('login/', Login.as_view(), name='login'),
    path('login/forget_password/', Forget_password.as_view(), name='forget_password'),
    path('logout/', logout, name='logout'),
     ]
