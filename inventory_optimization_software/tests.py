from django.test import TestCase
from .views import validate_item
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
