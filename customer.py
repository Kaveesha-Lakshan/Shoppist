from shop_algorithms import ProductHeap, CartManager
import heapq

products_heap = ProductHeap()
products_heap.load_from_file()
cart_mgr = CartManager()


def show_products():
    grouped = products_heap.show_all_grouped()
    if not grouped:
        print("No products available.")
        return
    print("\n Products:")
    for pn in sorted(grouped.keys()):
        for b, p, q in grouped[pn]:
            print(f"- {pn.capitalize()} ({b}): Rs{p:.2f} (Stock: {q})")

def search_products():
    kw = input("Keyword: ").strip()
    results = products_heap.search_by_keyword(kw)
    if not results:
        print("No matching products.")
        return
    print(f"\n Results for '{kw}':")
    for p, n, b, q in results:
        print(f"{n.title()} ({b}) — Rs{p:.2f} (Stock: {q})")

def add_to_cart():
    keyword = input("\nEnter search keyword: ").strip()
    results = products_heap.search_by_keyword(keyword)
    if not results:
        print(" No matching products found.")
        return
    print(f"\n Results for '{keyword}':")
    for idx, (price, name, brand, qty) in enumerate(results, start=1):
        print(f"{idx}. {name.title()} ({brand}) — Rs{price:.2f} (Stock: {qty})")

    try:
        selection = int(input("\nSelect product number to add (0 to cancel): ").strip())
    except ValueError:
        print(" Invalid input.")
        return
    if selection == 0:
        print("Cancelled.")
        return
    if not (1 <= selection <= len(results)):
        print(" Invalid choice.")
        return

    price, name, brand, stock = results[selection - 1]
    if stock <= 0:
        print(" Out of stock.")
        return

    try:
        qty = int(input(f"Enter quantity (Available: {stock}): ").strip())
    except ValueError:
        print(" Invalid quantity.")
        return
    if qty <= 0 or qty > stock:
        print(f" Invalid quantity. Available: {stock}")
        return

    if cart_mgr.add_item(name, brand, qty, products_heap):
        print(f" Added {qty} x {name.title()} ({brand}) to cart.")
    else:
        print(" Could not add to cart.")

def view_cart():
    if not cart_mgr.cart:
        print("\n Cart is empty.")
        return
    print("\n Cuerrent Cart:")
    heap_list = []
    total = 0
    for (n, b), qty in cart_mgr.cart.items():
        price = next((p for p, name, brand, _ in products_heap.heap if n == name and b == brand), None)
        if price is None:
            continue
        subtotal = price * qty
        heapq.heappush(heap_list, (subtotal, n, b, qty, price))
    while heap_list:
        subtotal, n, b, qty, price = heapq.heappop(heap_list)
        print(f"- {n.title()} ({b}) x {qty} @ Rs{price:.2f} = Rs{subtotal:.2f}")
        total += subtotal
    print(f"Total (current prices): ₹{total:.2f}")

def modify_cart():
    if not cart_mgr.cart:
        print("\n Cart is empty.")
        return
    print("\n Modify Cart Items:")
    for (n, b), qty in cart_mgr.cart.items():
        print(f"- {n.title()} ({b}): {qty} units")
    name = input("Product name to modify: ").strip().lower()
    brand = input("Brand: ").strip()
    if (name, brand) not in cart_mgr.cart:
        found = [(n, b) for (n, b) in cart_mgr.cart.keys() if n == name and b.lower() == brand.lower()]
        if found:
            name, brand = found[0]
        else:
            print(" Item not in cart.")
            return
    try:
        new_qty = int(input("New quantity (0 to remove): ").strip())
    except ValueError:
        print(" Invalid quantity.")
        return
    if cart_mgr.modify_item(name, brand, new_qty, products_heap):
        if new_qty == 0:
            print(" Removed item from cart.")
        else:
            print(" Cart updated.")
    else:
        print(" Update failed.")

def remove_from_cart():
    if not cart_mgr.cart:
        print("\n Cart is empty.")
        return
    print("\n Remove Item from Cart:")
    for idx, ((n, b), qty) in enumerate(cart_mgr.cart.items(), start=1):
        print(f"{idx}. {n.title()} ({b}) — {qty} units")
    try:
        choice = int(input("\nSelect item number to remove (0 to cancel): ").strip())
    except ValueError:
        print(" Invalid input.")
        return
    if choice == 0:
        print("Cancelled.")
        return
    if not (1 <= choice <= len(cart_mgr.cart)):
        print(" Invalid choice.")
        return
    selected_key = list(cart_mgr.cart.keys())[choice - 1]
    name, brand = selected_key
    cart_mgr.remove_item(name, brand, products_heap)
    print(f" Removed {name.title()} ({brand}) from cart.")

def checkout():
    cart_mgr.checkout(products_heap)


def main_menu():
    while True:
        print("\n--- Customer Menu ---")
        print("1. View products")
        print("2. Search product")
        print("3. Search and add to cart")
        print("4. Modify cart quantity")
        print("5. Remove from cart")
        print("6. View cart")
        print("7. Checkout")
        print("8. Exit")

        choice = input("Choose: ").strip()
        if choice == "1":
            show_products()
        elif choice == "2":
            search_products()
        elif choice == "3":
            add_to_cart()
        elif choice == "4":
            modify_cart()
        elif choice == "5":
            remove_from_cart()
        elif choice == "6":
            view_cart()
        elif choice == "7":
            checkout()
        elif choice == "8":
            print("Happy Shopping!")
            break
        else:
            print(" Invalid choice.")

if __name__ == "__main__":
    main_menu()
