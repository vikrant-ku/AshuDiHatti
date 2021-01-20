from django.shortcuts import render, get_object_or_404
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.product import Product, FbLive
from django.views import  View
from .home import prod_category, card_len
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage



class Shop(View):

    def get(self , request, **kwargs):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)

        path_info = request.path
        subcategory_name=None
        subcat_type_name=None
        category_name = kwargs['category']
        if 'subcat' in kwargs:
            subcategory_name = kwargs['subcat']
        if 'subcat_type' in kwargs:
            subcat_type_name = kwargs['subcat_type']


        color = request.GET.get('color')
        filter = request.GET.get('filterby')


        cat = get_object_or_404(Category, name=category_name)

        cat_name = category_name.capitalize() # for page-title
        sub_category = Subcategory.objects.filter(category=cat.id).distinct() # for side filter



        if subcategory_name != None:
            sub_cat = get_object_or_404(Subcategory, name=subcategory_name, category=cat.id)
            if subcat_type_name != None:
                if color and filter == "Low-to-High":
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id,subcat_type=subcat_type_name, color=color).order_by('discount_price')
                elif color and filter == "High-to-Low":
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id,subcat_type=subcat_type_name, color=color).order_by('-discount_price')
                elif color == None and filter == "Low-to-High":
                    all_prod = Product.objects.filter(category=cat.id,subcategory= sub_cat.id,subcat_type=subcat_type_name).order_by('discount_price')
                elif color == None and filter == "High-to-Low":
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id,subcat_type=subcat_type_name).order_by('-discount_price')
                elif color and filter == None:
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id,subcat_type=subcat_type_name, color=color)
                else:
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id, subcat_type=subcat_type_name )
            else:
                if color and filter == "Low-to-High":
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id, color=color).order_by('discount_price')
                elif color and filter == "High-to-Low":
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id, color=color).order_by('-discount_price')
                elif color == None and filter == "Low-to-High":
                    all_prod = Product.objects.filter(category=cat.id,subcategory= sub_cat.id).order_by('discount_price')
                elif color == None and filter == "High-to-Low":
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id).order_by('-discount_price')
                elif color and filter == None:
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id, color=color)
                else:
                    all_prod = Product.objects.filter(category=cat.id, subcategory=sub_cat.id)
        else:
            if color and filter == "Low-to-High":
                all_prod = Product.objects.filter(category=cat.id, color=color).order_by('discount_price')
            elif color and filter == "High-to-Low":
                all_prod = Product.objects.filter(category=cat.id, color=color).order_by('-discount_price')
            elif color == None and filter == "Low-to-High":
                all_prod = Product.objects.filter(category=cat.id).order_by('discount_price')
            elif color == None and filter == "High-to-Low":
                all_prod = Product.objects.filter(category=cat.id).order_by('-discount_price')
            elif color and filter == None:
                all_prod = Product.objects.filter(category=cat.id, color=color)
            else:
                all_prod = Product.objects.filter(category=cat.id)



        all_color = get_product_color(all_prod) # all available color for filter

        #paginator
        paginator = Paginator(all_prod, 6)
        page = request.GET.get('page')

        try:
            prods = paginator.page(page)
        except PageNotAnInteger:
            prods = paginator.page(1)
        except EmptyPage:
            prods = paginator.page(paginator.num_pages)

        if page is None:
            start_index = 0
            end_index= 7
        else:
            (start_index, end_index)=proper_pagination(prods, index=1)

        page_range = list(paginator.page_range)[start_index:end_index]

        my_product = {
            'category': category,
            'len': len_cart,

            'cat_name': cat_name,
            'sub_category': sub_category,

            'allprods': prods,
            'all_color':all_color,
            'path_info':path_info,

            'page_range': page_range,

            # 'subcategory':subcat,
            'color': color,
            'filter': filter,
                    }

        return render (request, 'shop/shop.html', my_product)
#
#
class Fbshop(View):
    def get(self, request, date=None):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)# header drop down

        dates = FbLive.objects.order_by('-date').values_list('date', flat=True).distinct()
        fbprod= ""

        if date:
            fbprod = FbLive.objects.filter(date= date)
            pass
        else:
            fbprod = FbLive.objects.all().order_by('-date')

        prod = []

        for _ in fbprod:
            prod.append(get_object_or_404(Product, sr_no=_.prodsr_no))



        paginator = Paginator(prod, 3)
        page = request.GET.get('page')

        try:
            prods = paginator.page(page)
        except PageNotAnInteger:
            prods = paginator.page(1)
        except EmptyPage:
            prods = paginator.page(paginator.num_pages)

        if page is None:
            start_index = 0
            end_index = 7
        else:
            (start_index, end_index) = proper_pagination(prods, index=1)

        page_range = list(paginator.page_range)[start_index:end_index]


        my_product = {
            'category': category,
            'len': len_cart,

            'allprods': prods,



            'date': dates,
            'page_range': page_range,
            'filterdate': date
        }
        return render(request, 'shop/fbshop.html', my_product)

def proper_pagination(prods, index):
    start_index = 0
    end_index = 7
    if prods.number > index:
        start_index = prods.number - index
        end_index = start_index + end_index
    return (start_index,end_index)


def get_product_color(prod_object):
    color = []
    for i in prod_object:
        if i.color not in color:
            color.append(i.color)
    return color