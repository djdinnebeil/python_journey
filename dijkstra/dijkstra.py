import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}
    distances[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        visited.add(current_node)
        print('visiting', current_node)
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            print('neighbor with weight', neighbor)
            if distance < distances[neighbor]:
                print('updating distance from', distances[neighbor], 'to', distance)
                print('updating parent from', previous[neighbor], 'to', current_node)
                distances[neighbor] = distance
                previous[neighbor] = current_node
                if neighbor not in visited:
                    heapq.heappush(heap, (distance, neighbor))

    return distances, previous

def reconstruct_path(previous, start, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path if path[0] == start else []

def print_all_paths(graph, start):
    distances, previous = dijkstra(graph, start)
    print(distances, previous)
    print(f"Shortest distances from '{start}':")
    for node in distances:
        print(f"  {node}: {distances[node]}")
    print("\nShortest paths from '{}':".format(start))
    for node in graph:
        path = reconstruct_path(previous, start, node)
        if path:
            print(f"  {node}: {' -> '.join(path)}")
        else:
            print(f"  {node}: unreachable")

# Example graph
graph = {
    'A': [('B', 2), ('C', 1), ('D', 10)],
    'B': [('C', 2), ('D', 5)],
    'C': [('D', 5)],
    'D': [],
    'T': []
}

# Run
print_all_paths(graph, 'A')
