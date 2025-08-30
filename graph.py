import heapq

class SupermarketGraph:
    def __init__(self):
        self.graph = {}

    def add_connection(self, from_rack, to_rack, distance):
        self.graph.setdefault(from_rack, []).append((to_rack, distance))
        self.graph.setdefault(to_rack, []).append((from_rack, distance))

def dijkstra_path(graph, start, target):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node == target:
            break
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    node = target
    while node is not None:
        path.insert(0, node)
        node = previous[node]
    return path
