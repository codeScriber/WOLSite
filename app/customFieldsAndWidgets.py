from wtforms.widgets import Input
from wtforms.fields import StringField
from wtforms.widgets import HTMLString

class InputWithAF(Input):
    def __init__(self, input_type=None):
        super(InputWithAF, self).__init__(input_type)

    def __call__(self, field, **kwargs):
        autofocus = kwargs.pop('autofocus','')
        autofocus = True if autofocus in ['True', 'true', 'yes'] else False
        widget_str = super(InputWithAF, self).__call__(field, **kwargs)
        if autofocus:
            widget_str = HTMLString('%s autofocus>' % widget_str[:-1])
        return widget_str


class StringFieldWithAF(StringField):
    widget = InputWithAF('text')