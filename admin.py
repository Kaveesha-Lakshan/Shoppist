
from shop_algorithms import ProductHeap
import json
from product_assigner import assign_products_to_racks

class InitAbort(Exception):
    """Raised when user types 'done' to abort layout setup."""
    pass


def generate_rack_ids(rows, cols):
    return [f"R{i+1}" for i in range(rows * cols)]

def parse_layout_size():
    """
    Prompt for layout size in rowsxcols format.
    If user enters 'done', abort initialization.
    """
    while True:
        raw = input(" Enter your layout size (e.g. 3x3) or 'done' to cancel: ").strip().lower()
        if raw == "done":
            raise InitAbort
        if 'x' in raw:
            try:
                rows, cols = map(int, raw.split('x'))
                return rows, cols
            except ValueError:
                print(" Invalid format. Use rowsxcols, e.g. 3x3.")
        else:
            print(" Missing 'x'. Please enter like 3x3 or type 'done' to cancel.")

def get_distance_input(a, b):
    """
    Prompt for distance between rack a and b.
    '0' or blank means no direct path.
    'done' aborts the entire initialization.
    """
    while True:
        raw = input(f" Distance {a} -> {b} (blank/0=no path, 'done'=cancel): ").strip().lower()
        if raw == "done":
            raise InitAbort
        if raw == "" or raw == "0":
            return float('inf')
        try:
            return float(raw)
        except ValueError:
            print(" Enter a number, 0/blank for no path, or 'done' to cancel.")

def collect_distances(rack_ids):
    """
    Build a symmetric distance map between all rack pairs.
    Aborts on 'done'.
    """
    distances = {}
    n = len(rack_ids)
    for i in range(n):
        for j in range(i+1, n):
            a, b = rack_ids[i], rack_ids[j]
            dist = get_distance_input(a, b)
            distances[(a, b)] = dist
            distances[(b, a)] = dist
    return distances

def save_layout(data, filename="layout_data.json"):
    # preserve existing inventory if present so we don't clobber product inventory
    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = {}

    if isinstance(existing, dict) and "inventory" in existing:
        # copy inventory into new data unless already provided
        data.setdefault("inventory", existing.get("inventory"))

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\nSaved layout to {filename}")

def initialize_layout():
    """
    Full layout initialization flow.
    Catches InitAbort and returns to admin menu.
    """
    try:
        # 1) parse and generate rack IDs
        rows, cols = parse_layout_size()
        rack_ids = generate_rack_ids(rows, cols)
        print(f"\n Generated racks: {rack_ids}\n")

        # 2) distances
        print(" Fill in distances between racks:")
        distances = collect_distances(rack_ids)

        # 3) product assignment
        print("\n Assign products to racks:")
        product_map = assign_products_to_racks(rack_ids)

        # 4) assemble and save
        layout_data = {
            "rack_ids": rack_ids,
            "distances": {
                f"{a}->{b}": ("∞" if d == float('inf') else d)
                for (a, b), d in distances.items()
            },
            "products": product_map
        }
        save_layout(layout_data)

    except InitAbort:
        print("\nLayout initialization canceled. Returning to Admin Menu.")

def run_admin_menu():
	products = ProductHeap()
	products.load_from_file("layout_data.json")

	while True:
		print("\n--- Admin Menu ---")
		print("1. Add product")
		print("2. Update product")
		print("3. Delete product")
		print("4. View all products")
		print("5. Initialize shop layout")
		print("6. Exit")

		choice = input("Choose: ").strip()
		if choice == "1":
			# add product
			name  = input("Product name: ").strip()
			brand = input("Brand: ").strip()
			try:
				price = float(input("Price: ").strip())
				qty   = int(input("Quantity: ").strip())
			except ValueError:
				print("Invalid input.")
				continue
			products.add_product(name, brand, price, qty)
			products.save_to_file("layout_data.json")
			print(f" Added {brand} {name} – Rs {price:.2f} (Qty: {qty})")

			# NEW: ask admin if they'd like to assign this product to a rack in layout_data.json
			assign = input("Assign this product to a rack? (y/N): ").strip().lower()
			if assign == "y":
				try:
					with open("layout_data.json", "r") as lf:
						layout = json.load(lf)
				except FileNotFoundError:
					print(" layout_data.json not found. Initialize layout first (Admin -> Initialize shop layout).")
				else:
					rack_ids = layout.get("rack_ids", [])
					products_map = layout.get("products", {})

					# display racks and current assignment
					print("\nAvailable racks and current assignments:")
					for r in rack_ids:
						current = products_map.get(r, "unassigned")
						print(f"  {r}: {current}")

					while True:
						rack_choice = input("Enter rack id to assign (or blank to cancel): ").strip().upper()
						if rack_choice == "":
							print(" Assignment canceled.")
							break
						if rack_choice not in rack_ids:
							print(" Invalid rack id. Choose from the list above.")
							continue
						# assign product name (store as provided name)
						products_map[rack_choice] = name
						layout["products"] = products_map
						save_layout(layout)
						print(f" Assigned product '{name}' to {rack_choice}.")
						break

		elif choice == "2":
			# update product
			name  = input("Name to update: ").strip()
			brand = input("Brand: ").strip()
			price = input("New price (blank skip): ").strip()
			qty   = input("New quantity (blank skip): ").strip()
			price_val = float(price) if price else None
			qty_val   = int(qty)   if qty   else None

			if products.update_product(name, brand, price_val, qty_val):
				products.save_to_file("layout_data.json")
				print(" Updated.")
			else:
				print(" Not found.")

		elif choice == "3":
			# delete product
			name  = input("Name to delete: ").strip()
			brand = input("Brand: ").strip()
			products.delete_product(name, brand)
			products.save_to_file("layout_data.json")
			print(" Deleted.")

		elif choice == "4":
			# view all grouped
			grouped = products.show_all_grouped()
			if not grouped:
				print("No products.")
			else:
				for pn in sorted(grouped.keys()):
					print(f"\n{pn.capitalize()}:")
					for b, p, q in grouped[pn]:
						print(f"  {b} – Rs {p:.2f} (Qty: {q})")

		elif choice == "5":
			# kick off layout initializer
			initialize_layout()

		elif choice == "6":
			break

		else:
			print("Invalid choice.")


if __name__ == "__main__":
    run_admin_menu()