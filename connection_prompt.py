def get_distance_input(rack_a, rack_b):
    """
    Prompt the user for the distance between two racks.
    Treats '0' or blank input as infinite (no direct path).
    """
    while True:
        raw = input(f"Distance from {rack_a} to {rack_b} (enter 0 or leave blank for no path): ").strip()
        
        if raw == "" or raw == "0":
            return float('inf')  
        try:
            return float(raw)
        except ValueError:
            print(" Invalid input. Please enter a number, 0, or leave blank.")


def collect_distances(rack_ids):
    """
    Collects pairwise distances between racks.
    Returns a dictionary of distances: { (rack_a, rack_b): distance }
    """
    distances = {}
    n = len(rack_ids)

    for i in range(n):
        for j in range(i + 1, n):
            rack_a = rack_ids[i]
            rack_b = rack_ids[j]
            distance = get_distance_input(rack_a, rack_b)
            distances[(rack_a, rack_b)] = distance
            distances[(rack_b, rack_a)] = distance  # Symmetric for undirected graph

    return distances


# Example usage 
if __name__ == "__main__":
    rack_ids = ["R1", "R2", "R3"]

    print("Enter distances between racks:")
    distance_map = collect_distances(rack_ids)

    print("\nFinal Distance Map:")
    for pair, dist in distance_map.items():
        print(f"{pair[0]} → {pair[1]}: {'∞' if dist == float('inf') else dist}")