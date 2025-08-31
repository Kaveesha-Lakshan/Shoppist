import json
from collections import defaultdict
import heapq

class CartManager:
    def __init__(self, cart_file="cart.json"):
        self.cart_file = cart_file
        self.cart = defaultdict(int)
        self.load_cart()

    def load_cart(self):
        try:
            with open(self.cart_file, "r") as f:
                data = json.load(f)
                for n, b, qty in data:
                    self.cart[(n, b)] = qty
        except FileNotFoundError:
            pass

    def save_cart(self):
        data = [(n, b, qty) for (n, b), qty in self.cart.items()]
        with open(self.cart_file, "w") as f:
            json.dump(data, f)

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
        print("\n Final Bill )")
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
            print(f"{n.title()} ({b}) x {qty} @ Rs{price:.2f} = Rs{subtotal:.2f}")
            total += subtotal
        print("-" * 40)
        print(f"Total: Rs{total:.2f}")
        print("Thank you for shopping!")
        self.cart.clear()
        self.save_cart()

