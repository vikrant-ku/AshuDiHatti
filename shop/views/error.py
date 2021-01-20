from django.shortcuts import render
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from .home import prod_category, card_len

def error_404(request, exception):
   length = card_len(request)
   category = prod_category(Category, Subcategory)

   context = {
      'category': category,
            'len': length,
      }
   return render(request,'shop/404.html', context)

def error_500(request):
   length = card_len(request)
   category = prod_category(Category, Subcategory)
   context = {
      'category': category,
      'len': length,
   }
   return render(request,'shop/500.html', context)
