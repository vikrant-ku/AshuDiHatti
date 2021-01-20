from django.shortcuts import render , redirect , HttpResponseRedirect
from django.views import View
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.product import Product

# Create your views here.
class Index(View):

       def get(self , request):
        length = card_len(request)
        category = prod_category(Category, Subcategory)
        cate = Category.objects.all()
        all_prod = []
        for _ in cate:
            prod = []
            pr = Product.objects.filter(category=_.id)
            if len(pr) > 0:
                prod.append(pr)
            if len(prod) > 0:
                all_prod.append(prod)

        NA_prod = threeprod(Product.objects.filter(type= "NA"))
        BS_prod = threeprod(Product.objects.filter(type='BS'))
        YML_prod = threeprod(Product.objects.all())

        cart_prod = {
            'category':category,
            'len': length,
            'all_prod': all_prod,
            'NA_prod':NA_prod,
            'BS_prod':BS_prod,
            'YML_prod':YML_prod,

        }
        return render(request, "shop/index.html", cart_prod)


def prod_category(Category,Subcategory):
    category_data = {}
    try:
        category = Category.objects.all()
        for cat in category:
            try:
                subcat_data = {}
                subcategory = Subcategory.objects.filter(category=cat.id).distinct()
                for subcat in subcategory:
                    try:
                        subcat_type= []
                        prod = Product.objects.filter(category=cat.id, subcategory=subcat.id).values_list('subcat_type', flat=True).distinct()
                        if len(prod) > 0:
                            subcat_type.append(prod)

                        subcat_data[subcat]=subcat_type
                    except:
                        pass
                category_data[cat]=subcat_data

            except:
                pass
    except:
        pass

    return category_data

def card_len(request):
    cart = 0
    try:
        cart = request.session.get("cart")
        if cart != None:
            return len(cart)
        else:
            cart= 0
            return cart
    except:
         return cart


def threeprod(prod_object):
    prod = []
    if len(prod_object) > 3:
        for i in range(3):
            prod.append(prod_object[i])
        return prod
    else:
        return prod_object




