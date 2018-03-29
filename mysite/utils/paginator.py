from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def page_list(request, obj_list, page_num=5, page_name='page'):
    """
    obj_list: list of objects
    page_num: number of items in each page
    page_name: query name of page number in request url
    """
    paginator = Paginator(obj_list, page_num)
    page = request.GET.get(page_name)
    page_obj_list = None
    try:
        page_obj_list = paginator.page(page)
    except PageNotAnInteger:
        page_obj_list = paginator.page(1)
    except EmptyPage:
        page_obj_list = paginator.page(paginator.num_pages)
    except:
        page_obj_list = None
    return page_obj_list
    