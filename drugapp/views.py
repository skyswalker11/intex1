from django.shortcuts import render

# Create your views here.

def indexPageView(request) :
    return render(request, 'drugapp/index.html')

def searchPageView(request) :
    return render(request, 'drugapp/search.html')

def drugPageView(request) :
    return render(request, 'drugapp/drug.html')

def prescriberPageView(request) :
    return render(request, 'drugapp/prescriber.html')

def editprescriberPageView(request) :
    return render(request, 'drugapp/editprescriber.html')