from shop_algorithms import ProductHeap, CartManager
from addproductList import get_customer_product_list
from customer_route import build_graph, find_optimal_route
import json
import heapq
import importlib
import runpy
import subprocess
import sys
import os

products_heap = ProductHeap()
products_heap.load_from_file("layout_data.json")
cart_mgr = CartManager()

def show_products():
    grouped = products_heap.show_all_grouped()
    if not grouped:
        print("No products available.")
        return

    print("\n Products:")
    for product_name in sorted(grouped.keys()):
        print(f"\nProduct Name: {product_name.title()}")
        print("Brands (sorted by price):")
        brand_heap = []
        for brand, price, qty in grouped[product_name]:
            heapq.heappush(brand_heap, (price, brand, qty))
        index = 1
        while brand_heap:
            price, brand, qty = heapq.heappop(brand_heap)
            print(f"   {index}. {brand} — Rs {price:.2f} (Stock: {qty})")
            index += 1

def search_products():
    while True:
        kw = input("\n Enter product keyword to search (or '0' to finish): ").strip()
        if kw == "0":
            print(" Finished searching.")
            break
        results = products_heap.search_by_keyword(kw)
        if not results:
            print(" No matching products.")
            continue
        grouped = {}
        for price, name, brand, qty in results:
            grouped.setdefault(name.lower(), []).append((brand, price, qty))
        print(f"\n Products:")
        for product_name in sorted(grouped.keys()):
            print(f"\nProduct Name: {product_name.title()}")
            print("Brands (sorted by price):")
            brand_heap = []
            for brand, price, qty in grouped[product_name]:
                heapq.heappush(brand_heap, (price, brand, qty))
            index = 1
            while brand_heap:
                price, brand, qty = heapq.heappop(brand_heap)
                print(f"   {index}. {brand} — Rs {price:.2f} (Stock: {qty})")
                index += 1

def add_to_cart():
    while True:
        keyword = input("\nEnter search keyword (or '0' to finish): ").strip()
        if keyword == "0":
            print(" Finished adding products to cart.")
            break
        results = products_heap.search_by_keyword(keyword)
        if not results:
            print(" No matching products found.")
            continue
        grouped = {}
        for price, name, brand, qty in results:
            grouped.setdefault(name.lower(), []).append((brand, price, qty))
        for product_name in sorted(grouped.keys()):
            print(f"\n Products:\n\nProduct Name: {product_name.title()}")
            print("Brands (sorted by price):")
            brand_heap = []
            for brand, price, qty in grouped[product_name]:
                heapq.heappush(brand_heap, (price, brand, qty))
            sorted_brands = []
            while brand_heap:
                price, brand, qty = heapq.heappop(brand_heap)
                sorted_brands.append((price, brand, qty))
                print(f"   {len(sorted_brands)}. {brand} — Rs {price:.2f} (Stock: {qty})")
            selected_indices = set()
            while True:
                try:
                    selection = int(input("\nSelect brand number to add (1 to N, 0 to skip): ").strip())
                    if selection == 0:
                        print(" Skipped remaining brands.")
                        break
                    if not (1 <= selection <= len(sorted_brands)):
                        print(" Invalid selection.")
                        continue
                    if selection in selected_indices:
                        print(" Already added this brand. Choose another.")
                        continue
                    selected_indices.add(selection)
                    price, brand, stock = sorted_brands[selection - 1]
                    qty = int(input(f"Enter quantity for {product_name.title()} ({brand}) (Available: {stock}): ").strip())
                    if qty <= 0 or qty > stock:
                        print(" Invalid quantity.")
                        continue
                    if cart_mgr.add_item(product_name, brand, qty, products_heap):
                        print(f" Added {qty} x {product_name.title()} ({brand}) to cart.")
                    else:
                        print(" Could not add to cart.")
                except ValueError:
                    print(" Invalid input. Try again.")
                    
import heapq  

def view_cart():
    if not cart_mgr.cart:
        print("\n Cart is empty.")
        return

    # 1. Build a flat list of all items with their computed subtotals
    items = []
    for (name, brand), qty in cart_mgr.cart.items():
        price = next(
            (p for p, n, b, _ in products_heap.heap
             if n == name and b == brand),
            None
        )
        if price is None:
            continue
        subtotal = price * qty
        items.append((subtotal, name, brand, qty, price))

    # 2. Sort items by subtotal (lowest first)
    items.sort(key=lambda x: x[0])

    # 3. Print in the flat 
    print("\n Current Cart:")
    total = 0.0
    for subtotal, name, brand, qty, price in items:
        print(f"          {name.title()} - {brand} x {qty} @ Rs {price:.2f} = Rs {subtotal:.2f}")
        total += subtotal

    print(f"\nTotal Bill :- Rs {total:.2f}")



def display_cart_with_indices(products_heap, cart_mgr):
    index_map = {}
    grouped_cart = {}
    for (name, brand), qty in cart_mgr.cart.items():
        price = next((p for p, n, b, _ in products_heap.heap if n == name and b == brand), None)
        if price is not None:
            subtotal = price * qty
            grouped_cart.setdefault(name.lower(), []).append((subtotal, price, brand, qty))

    print("\n Current Cart:")
    total = 0
    global_index = 1
    for product_name in sorted(grouped_cart.keys()):
        print(f"\nProduct Name:- {product_name.title()}")
        brand_heap = []
        for subtotal, price, brand, qty in grouped_cart[product_name]:
            heapq.heappush(brand_heap, (subtotal, price, brand, qty))

        while brand_heap:
            subtotal, price, brand, qty = heapq.heappop(brand_heap)
            print(f"   {global_index}. {brand} x {qty} @ RS {price:.2f} = Rs {subtotal:.2f}")
            index_map[global_index] = (product_name, brand)
            total += subtotal
            global_index += 1

    print(f"\nTotal Bill :- Rs {total:.2f}")
    return index_map

def cart_action_menu():
    while True:
        print("\n Cart Actions:")
        print("1.  Update cart item")
        print("2.  Remove cart item")
        print("0.  Back to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            index_map = display_cart_with_indices(products_heap, cart_mgr)
            if not index_map:
                print(" Cart is empty.")
                continue
            try:
                selection = int(input("\nSelect item number to update: ").strip())
                if selection not in index_map:
                    print(" Invalid selection.")
                else:
                    name, brand = index_map[selection]
                    new_qty = int(input(f"Enter new quantity for {name.title()} ({brand}): ").strip())
                    if new_qty <= 0:
                        print(" Quantity must be positive.")
                    elif cart_mgr.modify_item(name, brand, new_qty, products_heap):
                        print(f" Updated {name.title()} ({brand}) to quantity {new_qty}.")
                    else:
                        print(" Could not update item.")
                view_cart()
            except ValueError:
                print(" Invalid input. Please enter a number.")

        elif choice == "2":
            index_map = display_cart_with_indices(products_heap, cart_mgr)
            if not index_map:
                print(" Cart is empty.")
                continue
            try:
                selection = int(input("\nSelect item number to remove: ").strip())
                if selection not in index_map:
                    print(" Invalid selection.")
                else:
                    name, brand = index_map[selection]
                    cart_mgr.remove_item(name, brand, products_heap)
                    print(f" Removed {name.title()} ({brand}) from cart.")
                view_cart()
            except ValueError:
                print(" Invalid input. Please enter a number.")

        elif choice == "0":
            break
        else:
            print(" Invalid choice. Please try again.")


def customer_menu():
    while True:
        print("\n--- Customer Menu ---")
        print("1.  Add product list")
        print("2.  View products")
        print("3.  Search product")
        print("4.  Add to cart")
        print("5.  View cart")
        print("6.  Checkout")
        print("7.  Find the cashier")   
        print("0.  Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            shopping_list = get_customer_product_list()

            # compute and show route based on layout_data.json using customer_route functions
            if shopping_list:
                try:
                    with open("layout_data.json", "r") as f:
                        layout = json.load(f)
                    distance_map = layout.get("distances", {})
                    product_map = layout.get("products", {})
                    rack_ids = layout.get("rack_ids", [])

                    graph = build_graph(distance_map)
                    for node in rack_ids:
                        graph.setdefault(node, [])

                    racks_to_visit = []
                    missing = []
                    for product in shopping_list:
                        found = False
                        for rack, item in product_map.items():
                            if item.strip().lower() == product.strip().lower():
                                racks_to_visit.append(rack)
                                found = True
                                break
                        if not found:
                            missing.append(product)

                    if missing:
                        for m in missing:
                            print(f" Product '{m}' not found in layout.")

                    if racks_to_visit:
                        route, total_distance = find_optimal_route(graph, racks_to_visit)
                        if route:
                            print("\n Optimal route to follow:")
                            print(" -> ".join(route))
                            print(f" Total distance: {total_distance:.2f} units")
                        else:
                            print(" No route could be computed for the selected products.")
                    else:
                        print(" No valid products found in layout to compute a route.")
                except FileNotFoundError:
                    print(" Layout file not found. Cannot compute route.")
                except Exception as e:
                    print(f" Error computing route: {e}")

            #  adding items from shopping_list to cart
            for keyword in shopping_list:
                results = products_heap.search_by_keyword(keyword)
                if not results:
                    print(f"\n No match for '{keyword}'")
                    continue
                brand_heap = []
                for price, name, brand, qty in results:
                    if name.lower() == keyword.lower():
                        heapq.heappush(brand_heap, (price, brand, qty))
                if not brand_heap:
                    print(f"\n No exact match for '{keyword}'")
                    continue
                print(f"\nProduct Name: {keyword.title()}")
                print("    Brands (sorted by price):")
                sorted_brands = []
                while brand_heap:
                    price, brand, qty = heapq.heappop(brand_heap)
                    sorted_brands.append((price, brand, qty))
                for i, (price, brand, qty) in enumerate(sorted_brands, start=1):
                    print(f"       {i}. {brand} — Rs {price:.2f} (Stock: {qty})")
                selected_indices = set()
                while True:
                    try:
                        selection = int(input("\nSelect brand number to add (1 to N, 0 to skip): ").strip())
                        if selection == 0:
                            print(" Skipped remaining brands.")
                            break
                        if not (1 <= selection <= len(sorted_brands)):
                            print(" Invalid selection.")
                            continue
                        if selection in selected_indices:
                            print(" Already added this brand. Choose another.")
                            continue
                        selected_indices.add(selection)
                        price, brand, stock = sorted_brands[selection - 1]
                        qty = int(input(f"Enter quantity for {keyword.title()} ({brand}) (Available: {stock}): ").strip())
                        if qty <= 0 or qty > stock:
                            print(" Invalid quantity.")
                            continue
                        if cart_mgr.add_item(keyword, brand, qty, products_heap):
                            print(f" Added {qty} x {keyword.title()} ({brand}) to cart.")
                        else:
                            print(" Could not add to cart.")
                    except ValueError:
                        print(" Invalid input. Try again.")
        elif choice == "2":
            show_products()
        elif choice == "3":
            search_products()
        elif choice == "4":
            add_to_cart()
        elif choice == "5":
            view_cart()
            cart_action_menu()
        elif choice == "6":
            cart_mgr.checkout(products_heap)
        elif choice == "7":
            # Try to run reroute_to_r1 in several ways 
            try:
                # Try importing as a module and calling main()
                mod = importlib.import_module("reroute_to_r1")
                if hasattr(mod, "main"):
                    mod.main()
                else:
                    # if no main, try runpy as fallback
                    runpy.run_module("reroute_to_r1", run_name="__main__")
            except Exception:
                # Try running the file in the same directory
                script_path = os.path.join(os.path.dirname(__file__), "reroute_to_r1.py")
                try:
                    if os.path.isfile(script_path):
                        runpy.run_path(script_path, run_name="__main__")
                    else:
                        # launch as a separate process
                        subprocess.run([sys.executable, script_path], check=True)
                except Exception as e:
                    print(f" Error running reroute_to_r1: {e}")
        elif choice == "0":
            print(" Exiting. Thank you!")
            break

        else:
            print(" Invalid choice. Please try again.")


if __name__ == "__main__":
    customer_menu()