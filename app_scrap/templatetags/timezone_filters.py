from django import template
from django.utils import timezone
import pytz



register = template.Library()





@register.filter
def to_gmt6(value):
    if not value:
        return value
    try:
        gmt6 = pytz.timezone('Asia/Dhaka')  
        return value.astimezone(gmt6)
    except (pytz.UnknownTimeZoneError, ValueError):
        return value