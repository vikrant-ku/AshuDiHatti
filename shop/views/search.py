from django.views import  View
from django.shortcuts import render , redirect
from shop.models.category import Category
from shop.models.sub_category import Subcategory
from shop.models.product import Product
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .home import prod_category, card_len
from.shop import proper_pagination

class Search(View):

    def get(self , request ):
        len_cart = card_len(request)  # card len
        category = prod_category(Category, Subcategory)

        my_product = {}
        query = None
        query = request.GET.get('q')
        filter = request.GET.get('filterby')


        if query:
            if filter == 'Low-to-High':
                prod = Product.objects.filter(Q(name__icontains=query)
                                          |Q(subcat_type__icontains=query)
                                          |Q(category__name__icontains=query)
                                          |Q(subcategory__name__icontains=query)
                                          |Q(description__icontains=query)
                                          |Q(specification__icontains=query)).order_by('discount_price')
            elif filter == 'High-to-Low':
                prod = Product.objects.filter(Q(name__icontains=query)
                                              | Q(subcat_type__icontains=query)
                                              | Q(category__name__icontains=query)
                                              | Q(subcategory__name__icontains=query)
                                              | Q(description__icontains=query)
                                              | Q(specification__icontains=query)).order_by('-discount_price')
            else:
                prod = Product.objects.filter(Q(name__icontains=query)
                                              | Q(subcat_type__icontains=query)
                                              | Q(category__name__icontains=query)
                                              | Q(subcategory__name__icontains=query)
                                              | Q(description__icontains=query)
                                              | Q(specification__icontains=query))


            paginator = Paginator(prod, 6)
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


            my_product = {"allprods": prods,
                          "q": query,
                          'category': category,
                          'len': len_cart,
                          'filter':filter,
                          'page_range': page_range,
                          }
        return render(request, 'shop/search.html', my_product)

