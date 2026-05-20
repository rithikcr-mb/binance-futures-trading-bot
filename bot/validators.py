def validate_quantity(quantity: str) -> float:
    try:
        quantity = float(quantity)

        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        return quantity

    except ValueError:
        raise ValueError("Quantity must be a valid positive number")


def validate_price(price: str) -> float:
    try:
        price = float(price)

        if price <= 0:
            raise ValueError("Price must be greater than 0")

        return price

    except ValueError:
        raise ValueError("Price must be a valid positive number")


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()

    if not symbol:
        raise ValueError("Trading symbol cannot be empty")

    return symbol


def validate_side(side: str) -> str:
    side = side.upper()

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")

    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()

    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be MARKET or LIMIT")

    return order_type
