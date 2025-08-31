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
                new_price = price if price is not None else p
                new_qty = quantity if quantity is not None else q
                self.heap[i] = (new_price, n, b, new_qty)
                heapq.heapify(self.heap)
                return True
        return False

    def delete_product(self, name, brand):
        self.heap = [(p, n, b, q) for p, n, b, q in self.heap
                     if not (n == name.lower() and b.lower() == brand.lower())]
        heapq.heapify(self.heap)

    def update_quantity(self, name, brand, qty_change):
        for i, (p, n, b, q) in enumerate(self.heap):
            if n == name.lower() and b.lower() == brand.lower():
                self.heap[i] = (p, n, b, q + qty_change)
                heapq.heapify(self.heap)
                return True
        return False

    def get_sorted_products(self):
        return sorted(self.heap, key=lambda x: x[0])

    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        matches = [(p, n, b, q) for p, n, b, q in self.heap if keyword in n]
        return sorted(matches, key=lambda x: x[0])

    def show_all_grouped(self):
        temp = sorted(self.heap, key=lambda x: (x[1], x[0]))
        grouped = defaultdict(list)
        for p, n, b, q in temp:
            grouped[n].append((b, p, q))
        return grouped

    def save_to_file(self, filename="products.json"):
        data = [(p, n, b, q) for p, n, b, q in self.heap]
        with open(filename, "w") as f:
            json.dump(data, f)

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


