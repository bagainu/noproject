
# Helping functions for ImageField
def image_upload_to(instance, file_name):
    return '''images/{0}_{1}'''.format(instance.id, file_name)
