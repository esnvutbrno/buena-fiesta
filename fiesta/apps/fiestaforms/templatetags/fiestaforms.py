from django.forms import BoundField
from django import template

register = template.Library()


@register.filter
def as_widget_field(bf: BoundField):
    return bf.as_widget(attrs={
        'class': f"peer "
                 f"Forms__{bf.field.widget.input_type} "
                 f"Forms__input ",
        'placeholder': ' '
    })


@register.filter
def as_label(bf: BoundField):
    return bf.label_tag(
        attrs={
            'class': f"Forms__label "
                     f"Forms__label--{bf.field.widget.input_type} "
        }
    )