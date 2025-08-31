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
        matches = [(p, n, b, q) for p, n, b, q in self.heap if keyword in n]
        return sorted(matches, key=lambda x: x[0])

    def show_all_grouped(self):
        grouped = defaultdict(list)
        for p, n, b, q in sorted(self.heap, key=lambda x: (x[1], x[0])):
            grouped[n].append((b, p, q))
        return grouped

    def save_to_file(self, filename="products.json"):
        with open(filename, "w") as f:
            json.dump([(p, n, b, q) for p, n, b, q in self.heap], f)

    def load_from_file(self, filename="products.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for record in data:
                    if len(record) == 3:
                        p, n, b = record
                        q = 0
                    else:
                        p, n, b, q = record
                    heapq.heappush(self.heap, (p, n, b, q))
        except FileNotFoundError:
            pass


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
        if new_qty == 0:
            self.remove_item(name, brand, products_heap)
            return True
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
            print("Cart is empty.")
            return
        print("\n Final Bill (sorted by subtotal)")
        print("-" * 40)
        heap = []
        total = 0
        for (n, b), qty in self.cart.items():
            for price, name, brand, _ in products_heap.heap:
                if n == name and b == brand:
                    subtotal = price * qty
                    heapq.heappush(heap, (subtotal, n, b, qty, price))
        while heap:
            subtotal, n, b, qty, price = heapq.heappop(heap)
            print(f"{n.title()} ({b}) x {qty} @ Rs{price:.2f} = ₹{subtotal:.2f}")
            total += subtotal
        print("-" * 40)
        print(f"Total: Rs{total:.2f}")
        print(" Thank you for shopping!")
        self.cart.clear()
        self.save_cart()
