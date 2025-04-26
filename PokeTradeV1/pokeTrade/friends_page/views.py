from django.shortcuts import render

def index(request):
    template_data = {}
    template_data['title'] = 'Friends'
    return render(request, 'friends_page/index.html', {'template_data': template_data})
