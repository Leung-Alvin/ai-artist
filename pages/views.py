from django.shortcuts import render

def index(req):
    return render(req, 'pages/index.html')

def about(req):
    return render(req, 'pages/about.html')
