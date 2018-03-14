from django import forms
from django.utils import timezone


YEAR_CHOICES = [str(year) for year in range(timezone.now().year + 1, 1800, -1)]
EMPTY_LABEL = ("Choose Year", "Choose Month", "Choose Day")


class CustomSelectDateWidget(forms.SelectDateWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs, renderer, *args, **kwargs):
        output = super().render(name, value, attrs, renderer, *args, **kwargs)
        components = [item + '</select>' for item in output.strip(' ').split('</select>') if len(item) != 0]
        select_date_output = """<div class='row'>"""
        for item in components:
            select_date_output = select_date_output + """<div class='col-sm'>{0}</div>""".format(item)
        select_date_output = select_date_output + """</div>"""
        return select_date_output   
    