import heapq
import json
from collections import defaultdict

class ProductHeap:
    def __init__(self):
        self.heap = []

    def add_product(self, name, brand, price, quantity):
        heapq.heappush(self.heap, (price, name.lower(), brand, quantity))

    def update_product(self, name, brand, price=None, quantity=None):
        for i, (p, n, b, q) in enumerate(self.heap):
            if n == name.lower() and b.lower() == brand.lower():
                self.heap[i] = (
                    price if price is not None else p,
                    n,
                    b,
                    quantity if quantity is not None else q
                )
                heapq.heapify(self.heap)
                return True
        return False

    def delete_product(self, name, brand):
        self.heap = [
            (p, n, b, q)
            for p, n, b, q in self.heap
            if not (n == name.lower() and b.lower() == brand.lower())
        ]
        heapq.heapify(self.heap)

    def update_quantity(self, name, brand, qty_change):
        for i, (p, n, b, q) in enumerate(self.heap):
            if n == name.lower() and b.lower() == brand.lower():
                self.heap[i] = (p, n, b, q + qty_change)
                heapq.heapify(self.heap)
                return True
        return False

    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        return sorted([
            (p, n, b, q) for p, n, b, q in self.heap
            if keyword in n or keyword in b.lower()
        ], key=lambda x: x[0])

    def show_all_grouped(self):
        grouped = defaultdict(list)
        for p, n, b, q in sorted(self.heap, key=lambda x: (x[1], x[0])):
            grouped[n].append((b, p, q))
        return grouped

    def save_to_file(self, filename="layout_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # preserve existing keys, store inventory separately
        data["inventory"] = [(p, n, b, q) for p, n, b, q in self.heap]

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="layout_data.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        # reset current heap to avoid duplications on multiple loads
        self.heap.clear()

        records = None

        #  root is a list
        if isinstance(data, list):
            records = data
        #  inventory stored under "inventory" key
        elif isinstance(data, dict):
            if "inventory" in data:
                records = data["inventory"]
            elif "products" in data:
                # convert products mapping into inventory records
                products_map = data.get("products", {})
                records = []
                for rack, prod in products_map.items():
                    if not prod:
                        continue
                    prod_str = str(prod).strip()
                    if prod_str.lower() == "unassigned" or prod_str == "":
                        continue
                    # default price 0.0, brand "default", quantity 0
                    records.append((0.0, prod_str.lower(), "default", 0))
        if not records:
            return

        for record in records:
            # support record length 3 or 4
            if len(record) == 4:
                p, n, b, q = record
            elif len(record) == 3:
                p, n, b = record
                q = 0
            else:
                continue
            heapq.heappush(self.heap, (p, n, b, q))

class CartManager:
    def __init__(self, cart_file="cart.json"):
        self.cart_file = cart_file
        self.cart = defaultdict(int)
        self.load_cart()

    def load_cart(self):
        try:
            with open(self.cart_file, "r") as f:
                for n, b, qty in json.load(f):
                    self.cart[(n, b)] = qty
        except FileNotFoundError:
            pass

    def save_cart(self):
        with open(self.cart_file, "w") as f:
            json.dump([(n, b, qty) for (n, b), qty in self.cart.items()], f)

    def add_item(self, name, brand, qty, products_heap):
        if products_heap.update_quantity(name, brand, -qty):
            self.cart[(name, brand)] += qty
            self.save_cart()
            products_heap.save_to_file()
            return True
        return False

    def remove_item(self, name, brand, products_heap):
        if (name, brand) in self.cart:
            qty = self.cart[(name, brand)]
            products_heap.update_quantity(name, brand, qty)
            del self.cart[(name, brand)]
            self.save_cart()
            products_heap.save_to_file()

    def modify_item(self, name, brand, new_qty, products_heap):
        if (name, brand) not in self.cart:
            return False
        current = self.cart[(name, brand)]
        diff = new_qty - current
        if diff > 0:
            if not products_heap.update_quantity(name, brand, -diff):
                return False
        else:
            products_heap.update_quantity(name, brand, -diff)
        self.cart[(name, brand)] = new_qty
        self.save_cart()
        products_heap.save_to_file()
        return True
    def checkout(self, products_heap):
        if not self.cart:
            print("\n Cart is empty.")
            return

        # Build a flat list of all items with their computed subtotals
        items = []
        for (name, brand), qty in self.cart.items():
            price = next(
                (p for p, n, b, _ in products_heap.heap
                 if n == name and b == brand),
                None
            )
            if price is None:
                continue
            subtotal = price * qty
            items.append((subtotal, name, brand, qty, price))

        # Sort items by subtotal lowest first
        items.sort(key=lambda x: x[0])

        # Print in the flat 
        print("\n Products Bills:")
        total = 0.0
        for subtotal, name, brand, qty, price in items:
            print(f"   {name.title()} - {brand} x {qty} @ Rs {price:.2f} = Rs {subtotal:.2f}")
            total += subtotal

        # Print total and clear cart
        print(f"\nTotal Bill :- Rs {total:.2f}")
        print(" Checkout complete. Thank you for shopping!")

        # Persist changes clear cart & save files
        self.cart.clear()
        self.save_cart()
        products_heap.save_to_file()
