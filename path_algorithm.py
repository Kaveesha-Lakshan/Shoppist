import heapq

def shortest_path(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        dist, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]

        if node == end:
            return path, dist

        for neighbor, d in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (dist + d, neighbor, path))

    return None, float('inf')
