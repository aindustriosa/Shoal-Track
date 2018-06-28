from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def homepage(request):
    
    content_to_html = {'summary':[]
                       }

    return render(request, 'homepage.html', {'content': content_to_html})
