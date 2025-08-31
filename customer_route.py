import json
import heapq
import itertools

def build_graph(distance_map):
    graph = {}
    for key, value in distance_map.items():
        if "->" not in key:
            continue
        a, b = key.split("->", 1)
        graph.setdefault(a, [])
        graph.setdefault(b, [])  # ensure target node exists in graph
        weight = float('inf') if str(value) == "∞" else float(value)
        if weight != float('inf'):
            graph[a].append((b, weight))
    return graph

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    predecessors = {}
    if start not in distances:
        return distances, predecessors
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        cost, node = heapq.heappop(queue)
        if cost > distances.get(node, float('inf')):
            continue
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                predecessors[neighbor] = node
                heapq.heappush(queue, (new_cost, neighbor))
    return distances, predecessors

def reconstruct_path(predecessors, start, end):
    path = []
    node = end
    while node != start:
        path.append(node)
        node = predecessors.get(node)
        if node is None:
            return []
    path.append(start)
    return list(reversed(path))

def find_optimal_route(graph, racks):
    if not racks:
        return [], 0.0
    # precompute shortest paths and predecessors
    all_distances = {}
    all_predecessors = {}
    for rack in racks:
        dist, preds = dijkstra(graph, rack)
        all_distances[rack] = dist
        all_predecessors[rack] = preds

    min_distance = float('inf')
    best_sequence = []

    # try permutations fix first rack as start
    start = racks[0]
    for perm in itertools.permutations(racks[1:]):
        sequence = [start] + list(perm)
        total = 0
        valid = True
        for i in range(len(sequence) - 1):
            d = all_distances[sequence[i]].get(sequence[i + 1], float('inf'))
            if d == float('inf'):
                valid = False
                break
            total += d
        if valid and total < min_distance:
            min_distance = total
            best_sequence = sequence

    if not best_sequence:
        return [], float('inf')

    # build full route with intermediate nodes using predecessors
    full_route = [best_sequence[0]]
    for i in range(len(best_sequence) - 1):
        preds = all_predecessors[best_sequence[i]]
        hop = reconstruct_path(preds, best_sequence[i], best_sequence[i + 1])
        if not hop:
            # fallback to direct next rack if reconstruct fails
            full_route.append(best_sequence[i + 1])
        else:
            full_route.extend(hop[1:])  # skip duplicate
    return full_route, min_distance

def main():
    try:
        with open("layout_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("layout_data.json not found.")
        return

    rack_ids = data.get("rack_ids", [])
    distance_map = data.get("distances", {})
    product_map = data.get("products", {})

    graph = build_graph(distance_map)
    for node in rack_ids:
        graph.setdefault(node, [])

    print("\n🛒 CUSTOMER MODE: Enter products to buy (type 'done' to finish)")
    shopping_list = []
    while True:
        item = input("Product name: ").strip().lower()
        if item == "done":
            break
        if item:
            shopping_list.append(item)

    racks_to_visit = []
    for product in shopping_list:
        found = False
        for rack, item in product_map.items():
            if str(item).strip().lower() == product:
                racks_to_visit.append(rack)
                found = True
                break
        if not found:
            print(f"Product '{product}' not found")

    if not racks_to_visit:
        print(" No valid products found. Exiting.")
        return

    route, total_distance = find_optimal_route(graph, racks_to_visit)
    if not route:
        print("Could not compute an optimal route for the selected racks.")
        return

    print("\n Optimal route to follow:")
    print(" → ".join(route))
    print(f"✅ Total distance: {total_distance:.2f} units")

if __name__ == "__main__":
    main()
