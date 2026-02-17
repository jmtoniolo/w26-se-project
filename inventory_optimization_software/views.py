from django.shortcuts import render, redirect
from .models import Item


def index(request):
    if request.method == "POST":
        if request.POST.get("clear_button") == "clear_button":
            Item.objects.all().delete()
            return redirect("index")

        name = request.POST.get("itemname")
        qty = request.POST.get("itemquantity")
        if name and qty:
            Item.objects.create(name=name, qty=int(qty))
            return redirect("index")

    item_list = Item.objects.all()
    display = {
        "item_list": item_list,
    }
    return render(request, "inventorysplash.html", display)
