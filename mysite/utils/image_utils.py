from django import forms


# Helping functions for ImageField
def image_upload_to(instance, file_name):
    return '''images/{0}_{1}'''.format(instance.id, file_name)


class PreviewImageWidget(forms.ClearableFileInput):

    preview_template = """Preview: <img src='{0}' class='img-fluid img-thumbnail mt-1' style='display:block; max-width:100px; height:auto;' />"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def render(self, name, value, attrs, renderer, *args, **kwargs):
        output = super().render(name, value, attrs, renderer, *args, **kwargs)
        if value:
            return self.__class__.preview_template.format(value.url) + output
        return output

