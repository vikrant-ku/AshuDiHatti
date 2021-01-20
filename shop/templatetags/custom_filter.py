from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)



@register.filter(name='multiply')
def multiply(number , number1):
    return int(number) * int(number1)

@register.filter(name='calculatedate')
def caldate(date):
    a = datetime.now().date() - date.date()
    val = int(str(a)[0])
    return val


