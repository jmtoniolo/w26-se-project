class ItemConstraints:
    NAME_MAX_LENGTH = 29
    QTY_MIN = 0
    QTY_MAX = 999_999_999
    REORDER_LEVEL_MIN = 0
    REORDER_LEVEL_MAX = 999_999_999


class ErrorMessages:
    NAME_REQUIRED = "Name is required."
    QTY_REQUIRED = "Quantity is required."
    NAME_TOO_LONG = f"Name must be {ItemConstraints.NAME_MAX_LENGTH} characters or fewer."
    NAME_NOT_ASCII = "Name must contain only ASCII characters."
    QTY_NOT_INTEGER = "Quantity must be a whole number."
    QTY_NEGATIVE = f"Quantity cannot be below {ItemConstraints.QTY_MIN}."
    QTY_EXCEEDS_MAX = f"Quantity cannot exceed {ItemConstraints.QTY_MAX:,}."
    REORDER_NOT_INTEGER = "Reorder level must be a whole number."
    REORDER_NEGATIVE = f"Reorder level cannot be below {ItemConstraints.REORDER_LEVEL_MIN}."
    REORDER_EXCEEDS_MAX = f"Reorder level cannot exceed {ItemConstraints.REORDER_LEVEL_MAX:,}."
    NAME_DUPLICATE = "An item with that name already exists."
