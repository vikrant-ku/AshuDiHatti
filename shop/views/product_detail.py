from django.views import  View
from django.shortcuts import render, get_object_or_404
from shop.models.product import Product
from shop.models.category import Category
from shop.models.sub_category import Subcategory
# from .pages import card_len
from .home import prod_category, card_len

class Product_detail(View):
    def get(self , request, **kwargs):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)
        print(kwargs)
        slug = kwargs['slug']
        prod = get_object_or_404(Product, sr_no=slug)
        # prodname = prod.name
        # prodname = prodname.split("_")
        # related_prod = Product.objects.filter(name__icontains=prodname[0])
        #
        ids =[]
        try:
            if request.session.get("cart"):
                ids = list(request.session.get('cart').keys())
        except:
            pass
        flag = ""
        if str(prod.id) in ids:

            flag = 1
        my_product = {
            'category': category,
            'len': len_cart,
            'product': prod,
            # 'related_prod':related_prod
            'flag':flag,

                }
        return render(request , 'shop/product_view.html', my_product)
