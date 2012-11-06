from django import template


register = template.Library()


@register.inclusion_tag('image_uploader/cropping_preview.html', takes_context=False)
def cropping_preview(field, w, h):
    my_context = {}
    my_context['field'] = field
    my_context['w'] = w
    my_context['h'] = h
    return my_context
