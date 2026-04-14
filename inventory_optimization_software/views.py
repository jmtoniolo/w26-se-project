from urllib.parse import urlencode

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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


def validate_reorder_level(reorder_str):
    """Validate reorder level input. Returns (level_int, error_message) tuple."""
    if not reorder_str:
        return 0, None
    try:
        level = int(reorder_str)
    except ValueError:
        return None, ErrorMessages.REORDER_NOT_INTEGER
    if level < ItemConstraints.REORDER_LEVEL_MIN:
        return None, ErrorMessages.REORDER_NEGATIVE
    if level > ItemConstraints.REORDER_LEVEL_MAX:
        return None, ErrorMessages.REORDER_EXCEEDS_MAX
    return level, None


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

    # Check for error passed via query param (from edit/delete views)
    if error is None:
        error = request.GET.get("error", None)

    item_list = Item.objects.all()

    # Search (FR-17)
    search_query = request.GET.get("search", "").strip()
    if search_query:
        item_list = item_list.filter(name__icontains=search_query)

    # Sort (FR-21)
    sort_by = request.GET.get("sort", "")
    if sort_by == "name_asc":
        item_list = item_list.order_by("name")
    elif sort_by == "name_desc":
        item_list = item_list.order_by("-name")
    elif sort_by == "qty_asc":
        item_list = item_list.order_by("qty")
    elif sort_by == "qty_desc":
        item_list = item_list.order_by("-qty")
    elif sort_by == "id_asc":
        item_list = item_list.order_by("id")
    elif sort_by == "id_desc":
        item_list = item_list.order_by("-id")

    # Filter (FR-15)
    filter_by = request.GET.get("filter", "")
    if filter_by == "low_stock":
        item_list = item_list.filter(qty__lte=F("reorder_level"))

    display = {
        "item_list": item_list,
        "items_json": items_json,
        "error": error,
        "search_query": search_query,
        "sort_by": sort_by,
        "filter_by": filter_by,
    }
    return render(request, "inventorysplash.html", display)


def increment_item(request, item_id):
    if request.method == "POST":
        Item.objects.filter(
            id=item_id, qty__lt=ItemConstraints.QTY_MAX
        ).update(qty=F("qty") + 1)
    return redirect("index")


def decrement_item(request, item_id):
    if request.method == "POST":
        Item.objects.filter(
            id=item_id, qty__gt=ItemConstraints.QTY_MIN
        ).update(qty=F("qty") - 1)
    return redirect("index")


def edit_item(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, id=item_id)
        name = request.POST.get("itemname", "").strip()
        qty_str = request.POST.get("itemquantity", "").strip()
        reorder_str = request.POST.get("reorder_level", "0").strip()

        qty, error = validate_item(name, qty_str)
        if error:
            return redirect(reverse("index") + "?" + urlencode({"error": error}))

        reorder_level, error = validate_reorder_level(reorder_str)
        if error:
            return redirect(reverse("index") + "?" + urlencode({"error": error}))

        # Check for name conflict with other items
        if Item.objects.filter(name=name).exclude(id=item_id).exists():
            return redirect(reverse("index") + "?" + urlencode({"error": ErrorMessages.NAME_DUPLICATE}))

        item.name = name
        item.qty = qty
        item.reorder_level = reorder_level
        item.save()
    return redirect("index")


def delete_item(request, item_id):
    if request.method == "POST":
        Item.objects.filter(id=item_id).delete()
    return redirect("index")
