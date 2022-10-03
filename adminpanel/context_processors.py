def get_query_param(request):
    data = {}
    status = request.GET.get('status', None)
    if status is not None:
        data['status'] = status
    return data
