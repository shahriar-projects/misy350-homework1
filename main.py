# MISY350 - Homework 1: Coffee Shop Kiosk Inventory & Orders (CRUD)

# --------------------
# DATA MODEL (IN MEMORY)
# --------------------

inventory = [
    {"item_id": 1, "name": "Espresso", "unit_price": 2.50, "stock": 40},
    {"item_id": 2, "name": "Latte", "unit_price": 4.25, "stock": 25},
    {"item_id": 3, "name": "Cold Brew", "unit_price": 3.75, "stock": 30},
    {"item_id": 4, "name": "Mocha", "unit_price": 4.50, "stock": 20},
    {"item_id": 5, "name": "Blueberry Muffin", "unit_price": 2.95, "stock": 18},
]

orders = [
    {"order_id": "Order_101", "item_id": 2, "quantity": 2, "status": "Placed", "total": 8.50},
    {"order_id": "Order_102", "item_id": 3, "quantity": 1, "status": "Placed", "total": 3.75},
]


def find_inventory_item_by_id(search_item_id: int):
    """Return the inventory item dict if found, otherwise None."""
    for item in inventory:
        if item["item_id"] == search_item_id:
            return item
    return None


def find_item_id_by_name(search_name: str):
    """Return item_id if the item name exists, otherwise None."""
    for item in inventory:
        if item["name"].lower() == search_name.lower():
            return item["item_id"]
    return None


# --------------------
# CREATE
# --------------------

# Query 1: Place a new order for an item and quantity.
# 1. Input:
item_id = int(input("Enter the Item ID to order: "))
quantity = int(input("Enter the quantity: "))

# 2. Process: Validate and create order
inventory_item = find_inventory_item_by_id(item_id)

if inventory_item is None:
    # 3. Output:
    print("Error: Item ID not found. Order not placed.")
else:
    if quantity <= 0:
        print("Error: Quantity must be greater than 0. Order not placed.")
    elif inventory_item["stock"] < quantity:
        print("Error: Not enough stock available. Order not placed.")
    else:
        # Reduce stock
        inventory_item["stock"] -= quantity

        # Create order_id (simple unique approach)
        next_order_number = len(orders) + 101
        new_order_id = f"Order_{next_order_number}"

        # Calculate total
        total_price = quantity * inventory_item["unit_price"]

        # Record order
        new_order = {
            "order_id": new_order_id,
            "item_id": item_id,
            "quantity": quantity,
            "status": "Placed",
            "total": round(total_price, 2),
        }
        orders.append(new_order)

        # 3. Output:
        print(f"Order placed successfully! Order ID: {new_order_id}")
        print(f"Item: {inventory_item['name']}, Quantity: {quantity}, Total: ${new_order['total']}")
        print(f"Updated stock for {inventory_item['name']}: {inventory_item['stock']}")


# --------------------
# READ
# --------------------

# Query 2: View all orders placed for a particular item — prompt the user to enter the item name.
# 1. Input:
search_item_name = input("Enter the item name to search (e.g. 'Latte'): ")

# 2. Process: Find orders for item
search_item_id = find_item_id_by_name(search_item_name)

matching_orders = []
if search_item_id is not None:
    for order in orders:
        if order["item_id"] == search_item_id:
            matching_orders.append(order)

# 3. Output:
if search_item_id is None:
    print("Error: Item name not found.")
elif len(matching_orders) == 0:
    print(f"No orders found for item: {search_item_name}")
else:
    print(f"Orders for {search_item_name}:")
    for order in matching_orders:
        print(f"- {order['order_id']} | Qty: {order['quantity']} | Status: {order['status']} | Total: ${order['total']}")


# Query 3: Calculate and print the total number of orders placed for "Cold Brew".
# 1. Input:
target_item_name = "Cold Brew"

# 2. Process: Count orders
target_item_id = find_item_id_by_name(target_item_name)

cold_brew_order_count = 0
if target_item_id is not None:
    for order in orders:
        if order["item_id"] == target_item_id and order["status"] == "Placed":
            cold_brew_order_count += 1

# 3. Output:
print(f"Total number of orders placed for '{target_item_name}': {cold_brew_order_count}")


# --------------------
# UPDATE
# --------------------

# Query 4: Prompt the user to enter an item id and new quantity. Update the item stock quantity.
# 1. Input:
update_item_id = int(input("Enter ID of item to update: "))
new_stock = int(input("Enter new stock quantity: "))

# 2. Process: Validate and update stock
update_item = find_inventory_item_by_id(update_item_id)

if update_item is None:
    # 3. Output:
    print("Error: Item ID not found. Stock not updated.")
elif new_stock < 0:
    print("Error: Stock cannot be negative. Stock not updated.")
else:
    update_item["stock"] = new_stock
    # 3. Output:
    print(f"Stock updated successfully! {update_item['name']} now has stock: {update_item['stock']}")


# --------------------
# REMOVE / DELETE
# --------------------

# Query 5: Cancel an order and restore stock.
# 1. Input:
cancel_order_id = input("Enter Order ID to cancel: ")

# 2. Process: Cancel order and restore stock
order_to_cancel = None
for order in orders:
    if order["order_id"] == cancel_order_id:
        order_to_cancel = order
        break

if order_to_cancel is None:
    # 3. Output:
    print("Error: Order ID not found. No order cancelled.")
else:
    if order_to_cancel["status"] == "Cancelled":
        print("This order is already cancelled. No changes made.")
    else:
        order_to_cancel["status"] = "Cancelled"

        restore_item = find_inventory_item_by_id(order_to_cancel["item_id"])
        if restore_item is not None:
            restore_item["stock"] += order_to_cancel["quantity"]

        # 3. Output:
        print(f"Order {cancel_order_id} cancelled successfully.")
        if restore_item is not None:
            print(
                f"Restored {order_to_cancel['quantity']} to {restore_item['name']}. "
                f"New stock: {restore_item['stock']}"
            )