import heapq


products = {
    "Milk": {"price": 50, "stock": 10},
    "Bread": {"price": 40, "stock": 8},
    "Eggs": {"price": 60, "stock": 12},
    "Rice": {"price": 80, "stock": 15},
    "Sugar": {"price": 45, "stock": 10}
}


cart = {}


def show_products():
    print("\n Available Products:")
    for name, info in products.items():
        print(f"- {name}: Rs {info['price']} (Stock: {info['stock']})")


def add_to_cart():
    while True:
        show_products()
        item = input("\nEnter product name to add to cart (or type 'done' to finish): ").strip().title()
        if item == "Done":
            break
        if item in products:
            available = products[item]["stock"]
            if available == 0:
                print(" Out of stock.")
                continue
            try:
                qty = int(input(f"Enter quantity for {item} (Available: {available}): "))
                if qty <= 0:
                    print(" Quantity must be positive.")
                elif qty > available:
                    print(f" Requested quantity ({qty}) exceeds available stock ({available}). Item not added.")
                else:
                    cart[item] = cart.get(item, 0) + qty
                    products[item]["stock"] -= qty
                    print(f" Added {qty} x {item} to cart.")
            except ValueError:
                print(" Invalid quantity.")
        else:
            print(" Product not found.")


def modify_cart():
    if not cart:
        print("\n Cart is empty.")
        return
    print("\n Modify Cart Items:")
    for item, qty in cart.items():
        print(f"- {item}: {qty} units")
    item = input("Enter product name to modify: ").strip().title()
    if item in cart:
        try:
            new_qty = int(input(f"Enter new quantity for {item}: "))
            if new_qty < 0:
                print(" Quantity cannot be negative.")
            else:
                current_qty = cart[item]
                stock_adjustment = current_qty - new_qty
                products[item]["stock"] += stock_adjustment
                if new_qty == 0:
                    del cart[item]
                    print(f" Removed {item} from cart.")
                elif new_qty > products[item]["stock"] + current_qty:
                    print(f" Not enough stock to update {item} to {new_qty}.")
                    products[item]["stock"] -= stock_adjustment  # Revert stock change
                else:
                    cart[item] = new_qty
                    print(f" Updated {item} to {new_qty} units.")
        except ValueError:
            print(" Invalid input.")
    else:
        print(" Item not in cart.")


def print_sorted_bill():
    print("\n Final Bill (sorted by subtotal)")
    print("-" * 40)
    heap = []
    total = 0
    for item, qty in cart.items():
        price = products[item]["price"]
        subtotal = qty * price
        heapq.heappush(heap, (subtotal, item, qty, price))
    while heap:
        subtotal, item, qty, price = heapq.heappop(heap)
        print(f"{item} x {qty} @ Rs {price} = Rs {subtotal}")
        total += subtotal
    print("-" * 40)
    print(f"Total Amount: Rs {total}")
    print(" Thank you for shopping!")


add_to_cart()
modify_cart()
print_sorted_bill()
