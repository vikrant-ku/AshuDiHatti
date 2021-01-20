from django import template

register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)[0]
    return 0


@register.filter(name='price_total')
def price_total(product, cart):
    if product.discount_price != 0:
        price = product.discount_price
    else:
        price = product.price
    return int(price) * int(cart_quantity(product, cart))


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    print(f"product{products}")
    for p in products:

        sum += price_total(p, cart)

    return sum
