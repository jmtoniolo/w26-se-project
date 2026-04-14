from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("increment/<int:item_id>/", views.increment_item, name="increment_item"),
    path("decrement/<int:item_id>/", views.decrement_item, name="decrement_item"),
    path("edit/<int:item_id>/", views.edit_item, name="edit_item"),
    path("delete/<int:item_id>/", views.delete_item, name="delete_item"),
]
