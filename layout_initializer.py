# layout_initializer.py

import json
from connection_prompt import collect_distances
from product_assigner import assign_products_to_racks

def generate_rack_ids(rows, cols):
    return [f"R{i+1}" for i in range(rows * cols)]

def parse_layout_size():
    while True:
        raw = input(" Enter your layout size (e.g. 3x3): ").lower().strip()
        if 'x' in raw:
            try:
                rows, cols = map(int, raw.split('x'))
                return rows, cols
            except ValueError:
                print(" Invalid format. Please enter as rowsxcols (e.g. 3x3).")
        else:
            print("Missing 'x'. Format must be like 3x3.")

def save_to_json(data, filename="layout_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\nData saved to {filename}")

def main():
    rows, cols = parse_layout_size()
    rack_ids = generate_rack_ids(rows, cols)

    print(f"\n Generated Racks: {rack_ids}")
    print("\n Fill in distances between racks:")
    distance_map = collect_distances(rack_ids)

    print("\n Assign products to racks:")
    product_map = assign_products_to_racks(rack_ids)

    # Combine and save
    layout_data = {
        "rack_ids": rack_ids,
        "distances": {
            f"{a}->{b}": ("∞" if dist == float('inf') else dist)
            for (a, b), dist in distance_map.items()
        },
        "products": product_map
    }

    save_to_json(layout_data)

if __name__ == "__main__":
    main()
