from django.shortcuts import render, redirect
from .models import Item
from .constants import ItemConstraints, ErrorMessages


def validate_item(name, qty_str):
    """Validate item input. Returns (qty_int, error_message) tuple."""
    if not name:
        return None, ErrorMessages.NAME_REQUIRED
    if not qty_str:
        return None, ErrorMessages.QTY_REQUIRED
    if not all(ord(c) < 128 for c in name):
        return None, ErrorMessages.NAME_NOT_ASCII
    if len(name) > ItemConstraints.NAME_MAX_LENGTH:
        return None, ErrorMessages.NAME_TOO_LONG
    try:
        qty = int(qty_str)
    except ValueError:
        return None, ErrorMessages.QTY_NOT_INTEGER
    if qty < ItemConstraints.QTY_MIN:
        return None, ErrorMessages.QTY_NEGATIVE
    if qty > ItemConstraints.QTY_MAX:
        return None, ErrorMessages.QTY_EXCEEDS_MAX
    return qty, None


def index(request):
    error = None

    if request.method == "POST":
        if request.POST.get("clear_button") == "clear_button":
            Item.objects.all().delete()
            return redirect("index")

        name = request.POST.get("itemname", "").strip()
        qty_str = request.POST.get("itemquantity", "").strip()

        qty, error = validate_item(name, qty_str)
        if error is None:
            Item.objects.create(name=name, qty=qty)
            return redirect("index")

    item_list = Item.objects.all()
    display = {
        "item_list": item_list,
        "error": error,
    }
    return render(request, "inventorysplash.html", display)
