from path_algorithm import shortest_path

# Store layout with distances
store = {
    "1": [("2", 2), ("3", 4)],
    "2": [("1", 2), ("4", 3), ("5", 6)],
    "3": [("1", 4), ("6", 5)],
    "4": [("2", 3)],
    "5": [("2", 6), ("7", 2), ("Cashier", 4)],
    "6": [("3", 5), ("Cashier", 3)],
    "7": [("5", 2)],
    "Cashier": [("5", 4), ("6", 3)]
}

print("Welcome to the Supermarket Assistant!")
rack_number = input("Please enter your current rack number: ").strip()

path, total_distance = shortest_path(store, rack_number, "Cashier")

if path:
    print("\nShortest path to cashier:")
    print(" -> ".join(path))
    print(f"Total distance: {total_distance} meters")
else:
    print("No path found from your location to the cashier.")
