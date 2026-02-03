from strands import tool

IN_MEMORY_ORDERS = {
    "A123": "Packed",
    "B456": "Shipped",
    "C789": "Delivered",
}


@tool
def get_order_status(order_id: str) -> str:
    """Return the status of an order ID from in-memory data."""
    if order_id in IN_MEMORY_ORDERS:
        return IN_MEMORY_ORDERS[order_id]
    return "Order not found"
