# supermarket_graph.py

class SupermarketGraph:
    def __init__(self):
        self.graph = {}
        self.products = {}

    def add_connection(self, from_rack, to_rack, distance):
        if from_rack not in self.graph:
            self.graph[from_rack] = {}
        self.graph[from_rack][to_rack] = distance

    def assign_product(self, rack, product_name):
        self.products[rack] = product_name

    def display(self):
        print("\n📊 Rack Connections:")
        for rack, connections in self.graph.items():
            for target, dist in connections.items():
                print(f"{rack} → {target} : {dist}")

        print("\n🛒 Product Assignments:")
        for rack, product in self.products.items():
            print(f"{rack} : {product}")
