from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render

def index(request):
    # This renders the 'base.html' template we created earlier
    #return HttpResponse("Hello, world, I'm iOS. I optimize inventories!")
    return render(request, 'inventorysplash.html')

def add_item(request):
    # This is a placeholder for your "Add" logic
    return render(request, 'add_item.html')

# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world, I'm iOS. I optimize inventories!")
