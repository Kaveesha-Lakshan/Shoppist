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

