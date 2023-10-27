from django.http import HttpResponse

def my_view(request):
    domain = request.META['HTTP_HOST']
    return HttpResponse(f"Домен сайта: {domain}")
