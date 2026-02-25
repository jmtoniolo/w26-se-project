from django.shortcuts import render, redirect
from django.db.models import F
from django.http import JsonResponse
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
            updated = Item.objects.filter(
                name=name, qty__lte=ItemConstraints.QTY_MAX - qty
            ).update(qty=F("qty") + qty)
            if updated:
                return redirect("index")
            if Item.objects.filter(name=name).exists():
                error = ErrorMessages.QTY_EXCEEDS_MAX
            else:
                Item.objects.create(name=name, qty=qty)
                return redirect("index")

    # Always get all items for client-side filtering
    item_list = Item.objects.all().order_by("name")
    
    # Convert items to JSON for client-side filtering
    items_json = [{"id": item.id, "name": item.name, "qty": item.qty} for item in item_list]

    display = {
        "item_list": item_list,
        "items_json": items_json,
        "error": error,
    }
    return render(request, "inventorysplash/inventorysplash.html", display)
