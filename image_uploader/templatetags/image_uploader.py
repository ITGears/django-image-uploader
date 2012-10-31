from django import template
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe


register = template.Library()

class CroppingPreviewNode(template.Node):
    def __init__(self, id_var, width_var, height_var):
        self.id_var = id_var
        self.width_var, self.height_var = width_var, height_var
        
    def render(self, context):
        try:
            id = int(self.id_var)
        except ValueError:
            id = context.get(self.id_var, 0)
            
        try:
            width, height = int(self.width_var), int(self.height_var)
        except ValueError:
            width, height = context.get(self.width_var, 0), context.get(self.height_var, 0) 
        
        t = get_template('image_uploader/cropping_preview.html')
        return t.render(Context({'id': id, 
                                 'w': width, 
                                 'h': height}))


@register.tag
def cropping_preview(parser, token):
    try:
        tag_name, id_var, width_var, height_var = token.contents.split(None, 3)
    except ValueError:
        msg = '%r tag requires arguments' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return CroppingPreviewNode(id_var, width_var, height_var)
