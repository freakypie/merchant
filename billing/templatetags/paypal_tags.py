'''
Template tags for paypal offsite payments
'''
from paypal.standard.forms import PayPalPaymentsForm
from django import template
from django.template.loader import render_to_string

register = template.Library()

class PayPalNode(template.Node):
    def __init__(self, integration):
        self.integration = template.Variable(integration)

    def render(self, context):
        int_obj = self.integration.resolve(context)
        form_str = render_to_string("billing/paypal.html", 
                                    {"form": PayPalPaymentsForm(initial=int_obj.fields),
                                     "integration": int_obj}, context)
        return form_str

@register.tag
def paypal(parser, token):
    try:
        tag, int_obj = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r was expecting a single argument" %token.split_contents()[0])
    return PayPalNode(int_obj)
