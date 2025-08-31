import json
import heapq

def build_graph(distance_map):
    graph = {}
    for key, value in distance_map.items():
        a, b = key.split("->")
        if a not in graph:
            graph[a] = []
        try:
            weight = float('inf') if str(value) == "∞" else float(value)
        except ValueError:
            weight = float('inf')
        if weight != float('inf'):
            graph[a].append((b, weight))
    return graph

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == end:
            return path, cost

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))

    return None, float('inf')

def main():
    # Load layout data
    with open("layout_data.json", "r") as f:
        data = json.load(f)

    rack_ids = data["rack_ids"]
    distance_map = data["distances"]

    # Normalize distances
    distance_map = {
        k: float('inf') if v == "∞" else float(v)
        for k, v in distance_map.items()
    }

    graph = build_graph(distance_map)

    print("\nREROUTE MODE: Enter your current rack (e.g., R6)")
    current_rack = input("Current rack: ").strip().upper()

    if current_rack not in rack_ids:
        print(f"Rack '{current_rack}' not found in layout.")
        return

    path, total_distance = dijkstra(graph, current_rack, "R1")

    if path:
        print("\nShortest path to R1:")
        print(" → ".join(path))
        print(f"Total distance: {total_distance} units")

        # Optional: show tree format
        tree_edges = [f"({path[i]} → {path[i+1]})" for i in range(len(path)-1)]
        tree_str = "Path to Cashier  = {" + ", ".join(tree_edges) + "}"
        print(tree_str)
    else:
        print("Invalid input.")

if __name__ == "__main__":
    main()