# myapp/templatetags/my_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """
    Mengalikan nilai dengan argumen.
    Contoh penggunaan: {{ some_value|mul:0.5 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return '' # Atau bisa juga 0 atau value, tergantung kebutuhan error handling Anda