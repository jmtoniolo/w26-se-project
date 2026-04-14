from django.test import TestCase, Client
from django.urls import reverse
from .views import validate_item, validate_reorder_level
from .models import Item
from .constants import ItemConstraints, ErrorMessages


class ValidateItemTest(TestCase):

    # --- Valid inputs ---

    def test_valid_input(self):
        qty, err = validate_item("Widget", "10")
        self.assertEqual(qty, 10)
        self.assertIsNone(err)

    def test_qty_zero(self):
        qty, err = validate_item("Widget", "0")
        self.assertEqual(qty, 0)
        self.assertIsNone(err)

    def test_qty_max_boundary(self):
        qty, err = validate_item("Widget", str(ItemConstraints.QTY_MAX))
        self.assertEqual(qty, ItemConstraints.QTY_MAX)
        self.assertIsNone(err)

    def test_name_exactly_max_length(self):
        name = "a" * ItemConstraints.NAME_MAX_LENGTH
        qty, err = validate_item(name, "1")
        self.assertEqual(qty, 1)
        self.assertIsNone(err)

    def test_name_single_char(self):
        qty, err = validate_item("A", "1")
        self.assertEqual(qty, 1)
        self.assertIsNone(err)

    # --- Name validation ---

    def test_empty_name(self):
        qty, err = validate_item("", "10")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.NAME_REQUIRED)

    def test_name_too_long(self):
        name = "a" * (ItemConstraints.NAME_MAX_LENGTH + 1)
        qty, err = validate_item(name, "10")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.NAME_TOO_LONG)

    def test_name_non_ascii(self):
        qty, err = validate_item("Widgét", "10")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.NAME_NOT_ASCII)

    # --- Quantity validation ---

    def test_empty_qty(self):
        qty, err = validate_item("Widget", "")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.QTY_REQUIRED)

    def test_qty_negative(self):
        qty, err = validate_item("Widget", "-1")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.QTY_NEGATIVE)

    def test_qty_exceeds_max(self):
        qty, err = validate_item("Widget", str(ItemConstraints.QTY_MAX + 1))
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.QTY_EXCEEDS_MAX)

    def test_qty_decimal(self):
        qty, err = validate_item("Widget", "1.5")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.QTY_NOT_INTEGER)

    def test_qty_non_numeric(self):
        qty, err = validate_item("Widget", "abc")
        self.assertIsNone(qty)
        self.assertEqual(err, ErrorMessages.QTY_NOT_INTEGER)


class ValidateReorderLevelTest(TestCase):

    def test_valid_reorder_level(self):
        level, err = validate_reorder_level("10")
        self.assertEqual(level, 10)
        self.assertIsNone(err)

    def test_empty_reorder_level_defaults_to_zero(self):
        level, err = validate_reorder_level("")
        self.assertEqual(level, 0)
        self.assertIsNone(err)

    def test_reorder_level_zero(self):
        level, err = validate_reorder_level("0")
        self.assertEqual(level, 0)
        self.assertIsNone(err)

    def test_reorder_level_max(self):
        level, err = validate_reorder_level(str(ItemConstraints.REORDER_LEVEL_MAX))
        self.assertEqual(level, ItemConstraints.REORDER_LEVEL_MAX)
        self.assertIsNone(err)

    def test_reorder_level_negative(self):
        level, err = validate_reorder_level("-1")
        self.assertIsNone(level)
        self.assertEqual(err, ErrorMessages.REORDER_NEGATIVE)

    def test_reorder_level_exceeds_max(self):
        level, err = validate_reorder_level(str(ItemConstraints.REORDER_LEVEL_MAX + 1))
        self.assertIsNone(level)
        self.assertEqual(err, ErrorMessages.REORDER_EXCEEDS_MAX)

    def test_reorder_level_non_integer(self):
        level, err = validate_reorder_level("abc")
        self.assertIsNone(level)
        self.assertEqual(err, ErrorMessages.REORDER_NOT_INTEGER)

    def test_reorder_level_decimal(self):
        level, err = validate_reorder_level("5.5")
        self.assertIsNone(level)
        self.assertEqual(err, ErrorMessages.REORDER_NOT_INTEGER)


class IncrementDecrementTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.item = Item.objects.create(name="TestItem", qty=5)

    def test_increment(self):
        self.client.post(reverse("increment_item", args=[self.item.id]))
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, 6)

    def test_decrement(self):
        self.client.post(reverse("decrement_item", args=[self.item.id]))
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, 4)

    def test_decrement_at_zero_stays_zero(self):
        """FR-11: Decrement shall not reduce qty below 0."""
        self.item.qty = 0
        self.item.save()
        self.client.post(reverse("decrement_item", args=[self.item.id]))
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, 0)

    def test_increment_at_max_stays_at_max(self):
        """FR-8: Increment shall not exceed QTY_MAX."""
        self.item.qty = ItemConstraints.QTY_MAX
        self.item.save()
        self.client.post(reverse("increment_item", args=[self.item.id]))
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, ItemConstraints.QTY_MAX)

    def test_increment_nonexistent_item(self):
        response = self.client.post(reverse("increment_item", args=[9999]))
        self.assertEqual(response.status_code, 302)

    def test_decrement_nonexistent_item(self):
        response = self.client.post(reverse("decrement_item", args=[9999]))
        self.assertEqual(response.status_code, 302)

    def test_get_request_does_not_modify(self):
        self.client.get(reverse("increment_item", args=[self.item.id]))
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, 5)


class EditItemTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.item = Item.objects.create(name="Original", qty=10, reorder_level=5)

    def test_edit_name_and_qty(self):
        self.client.post(reverse("edit_item", args=[self.item.id]), {
            "itemname": "Updated",
            "itemquantity": "20",
            "reorder_level": "5",
        })
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated")
        self.assertEqual(self.item.qty, 20)

    def test_edit_reorder_level(self):
        self.client.post(reverse("edit_item", args=[self.item.id]), {
            "itemname": "Original",
            "itemquantity": "10",
            "reorder_level": "15",
        })
        self.item.refresh_from_db()
        self.assertEqual(self.item.reorder_level, 15)

    def test_edit_duplicate_name_rejected(self):
        Item.objects.create(name="Other", qty=1)
        self.client.post(reverse("edit_item", args=[self.item.id]), {
            "itemname": "Other",
            "itemquantity": "10",
            "reorder_level": "5",
        })
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Original")  # unchanged

    def test_edit_same_name_allowed(self):
        """Keeping the same name on edit should not trigger duplicate error."""
        self.client.post(reverse("edit_item", args=[self.item.id]), {
            "itemname": "Original",
            "itemquantity": "50",
            "reorder_level": "5",
        })
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, 50)

    def test_edit_invalid_qty_rejected(self):
        self.client.post(reverse("edit_item", args=[self.item.id]), {
            "itemname": "Original",
            "itemquantity": "-5",
            "reorder_level": "0",
        })
        self.item.refresh_from_db()
        self.assertEqual(self.item.qty, 10)  # unchanged

    def test_edit_nonexistent_item_returns_404(self):
        response = self.client.post(reverse("edit_item", args=[9999]), {
            "itemname": "Ghost",
            "itemquantity": "1",
            "reorder_level": "0",
        })
        self.assertEqual(response.status_code, 404)

    def test_edit_updates_timestamp(self):
        """FR-22: Editing should update the updated_at timestamp."""
        old_updated = self.item.updated_at
        self.client.post(reverse("edit_item", args=[self.item.id]), {
            "itemname": "Original",
            "itemquantity": "99",
            "reorder_level": "0",
        })
        self.item.refresh_from_db()
        self.assertGreater(self.item.updated_at, old_updated)


class DeleteItemTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.item = Item.objects.create(name="ToDelete", qty=1)

    def test_delete_item(self):
        self.client.post(reverse("delete_item", args=[self.item.id]))
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_delete_nonexistent_item(self):
        response = self.client.post(reverse("delete_item", args=[9999]))
        self.assertEqual(response.status_code, 302)

    def test_id_not_reused_after_delete(self):
        """FR-5: Deleted IDs shall not be reused."""
        deleted_id = self.item.id
        self.client.post(reverse("delete_item", args=[self.item.id]))
        new_item = Item.objects.create(name="NewItem", qty=1)
        self.assertNotEqual(new_item.id, deleted_id)

    def test_get_request_does_not_delete(self):
        self.client.get(reverse("delete_item", args=[self.item.id]))
        self.assertTrue(Item.objects.filter(id=self.item.id).exists())


class LowStockDetectionTest(TestCase):

    def test_low_stock_when_qty_equals_reorder_level(self):
        """FR-19: Flagged when qty == reorder_level."""
        item = Item.objects.create(name="A", qty=5, reorder_level=5)
        self.assertTrue(item.is_low_stock)

    def test_low_stock_when_qty_below_reorder_level(self):
        """FR-19: Flagged when qty < reorder_level."""
        item = Item.objects.create(name="B", qty=3, reorder_level=10)
        self.assertTrue(item.is_low_stock)

    def test_not_low_stock_when_qty_above_reorder_level(self):
        item = Item.objects.create(name="C", qty=20, reorder_level=5)
        self.assertFalse(item.is_low_stock)

    def test_default_reorder_level_zero_not_low_stock(self):
        """With default reorder_level=0 and qty>0, should not be low stock."""
        item = Item.objects.create(name="D", qty=1)
        self.assertFalse(item.is_low_stock)

    def test_qty_zero_is_out_of_stock_not_low_stock(self):
        """qty=0 → out of stock, not low stock."""
        item = Item.objects.create(name="E", qty=0)
        self.assertTrue(item.is_out_of_stock)
        self.assertFalse(item.is_low_stock)


class SearchFilterSortTest(TestCase):

    def setUp(self):
        self.client = Client()
        Item.objects.create(name="Alpha", qty=100, reorder_level=5)
        Item.objects.create(name="Beta", qty=3, reorder_level=10)
        Item.objects.create(name="Gamma", qty=50, reorder_level=5)

    def test_search_by_name(self):
        """FR-17: Search by name."""
        response = self.client.get(reverse("index"), {"search": "alpha"})
        self.assertContains(response, "Alpha")
        self.assertNotContains(response, "Beta")
        self.assertNotContains(response, "Gamma")

    def test_search_case_insensitive(self):
        response = self.client.get(reverse("index"), {"search": "BETA"})
        self.assertContains(response, "Beta")

    def test_search_no_results(self):
        response = self.client.get(reverse("index"), {"search": "nonexistent"})
        self.assertContains(response, "No items in inventory")

    def test_sort_name_asc(self):
        """FR-21: Sort alphabetically ascending."""
        response = self.client.get(reverse("index"), {"sort": "name_asc"})
        content = response.content.decode()
        self.assertLess(content.index("Alpha"), content.index("Beta"))
        self.assertLess(content.index("Beta"), content.index("Gamma"))

    def test_sort_name_desc(self):
        response = self.client.get(reverse("index"), {"sort": "name_desc"})
        content = response.content.decode()
        self.assertLess(content.index("Gamma"), content.index("Beta"))
        self.assertLess(content.index("Beta"), content.index("Alpha"))

    def test_sort_qty_asc(self):
        """FR-21: Sort by quantity ascending."""
        response = self.client.get(reverse("index"), {"sort": "qty_asc"})
        content = response.content.decode()
        self.assertLess(content.index("Beta"), content.index("Gamma"))
        self.assertLess(content.index("Gamma"), content.index("Alpha"))

    def test_sort_qty_desc(self):
        response = self.client.get(reverse("index"), {"sort": "qty_desc"})
        content = response.content.decode()
        self.assertLess(content.index("Alpha"), content.index("Gamma"))
        self.assertLess(content.index("Gamma"), content.index("Beta"))

    def test_filter_low_stock(self):
        """FR-15/FR-19: Filter to show only low stock items."""
        response = self.client.get(reverse("index"), {"filter": "low_stock"})
        self.assertContains(response, "Beta")       # qty=3 <= reorder=10
        self.assertNotContains(response, "Alpha")    # qty=100 > reorder=5
        self.assertNotContains(response, "Gamma")    # qty=50 > reorder=5

    def test_search_and_sort_combined(self):
        response = self.client.get(reverse("index"), {"search": "alph", "sort": "name_asc"})
        self.assertContains(response, "Alpha")
        self.assertNotContains(response, "Gamma")


class StockUpdateValidationTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_cannot_create_item_with_negative_qty(self):
        """FR-20: Stock quantities cannot go below zero."""
        response = self.client.post(reverse("index"), {
            "itemname": "Test",
            "itemquantity": "-1",
        })
        self.assertFalse(Item.objects.filter(name="Test").exists())

    def test_decrement_does_not_go_below_zero(self):
        """FR-20: Decrement cannot result in negative value."""
        item = Item.objects.create(name="ZeroItem", qty=0)
        self.client.post(reverse("decrement_item", args=[item.id]))
        item.refresh_from_db()
        self.assertEqual(item.qty, 0)

    def test_edit_cannot_set_negative_qty(self):
        """FR-20: Edit cannot set qty to negative."""
        item = Item.objects.create(name="EditTest", qty=5)
        self.client.post(reverse("edit_item", args=[item.id]), {
            "itemname": "EditTest",
            "itemquantity": "-10",
            "reorder_level": "0",
        })
        item.refresh_from_db()
        self.assertEqual(item.qty, 5)  # unchanged


class TimestampTest(TestCase):

    def test_created_at_set_on_creation(self):
        """FR-22: Timestamp recorded when item is added."""
        item = Item.objects.create(name="Stamped", qty=1)
        self.assertIsNotNone(item.created_at)

    def test_updated_at_changes_on_edit(self):
        """FR-22: Timestamp updated when item is edited."""
        item = Item.objects.create(name="Stamped", qty=1)
        old_ts = item.updated_at
        item.qty = 2
        item.save()
        self.assertGreater(item.updated_at, old_ts)
