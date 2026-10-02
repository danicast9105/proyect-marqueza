from decimal import Decimal, InvalidOperation
from datetime import date


def positive_id(value):
    if isinstance(value, bool):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if parsed < 1 or not str(value).strip().isdigit():
        return None
    return parsed


def optional_id(value, field):
    if value in (None, ""):
        return None, None
    parsed = positive_id(value)
    if parsed is None:
        return None, (
            {"mensaje": f"El campo {field} debe ser un ID entero positivo"},
            400,
        )
    return parsed, None


def required_fields(data, fields):
    missing = [
        field for field in fields
        if data.get(field) is None
        or (isinstance(data.get(field), str) and not data[field].strip())
    ]
    if missing:
        return {"mensaje": "Faltan campos obligatorios", "campos": missing}, 400
    return None


def non_negative_number(value, field, integer=False, strictly_positive=False):
    if isinstance(value, bool) or value is None or value == "":
        return None, {"mensaje": f"El campo {field} debe ser un numero valido"}, 400
    try:
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None, {"mensaje": f"El campo {field} debe ser un numero valido"}, 400
    if not number.is_finite() or number < 0 or (strictly_positive and number == 0):
        return None, {"mensaje": f"El campo {field} debe ser mayor que cero" if strictly_positive else f"El campo {field} no puede ser negativo"}, 400
    if integer and number != number.to_integral_value():
        return None, {"mensaje": f"El campo {field} debe ser un entero"}, 400
    return int(number) if integer else float(number), None, None


def valid_date(value, field="fecha"):
    if not isinstance(value, str):
        return {"mensaje": f"El campo {field} debe tener formato YYYY-MM-DD"}, 400
    try:
        date.fromisoformat(value)
    except ValueError:
        return {"mensaje": f"El campo {field} debe tener formato YYYY-MM-DD"}, 400
    return None
