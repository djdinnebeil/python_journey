def dijkstra_v1(graph, start):
    import heapq
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))

    return distances

def dijkstra_v2(graph, start):
    import heapq
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    heap = [(0, start)]

    while heap:
        current_distance, current_node = heapq.heappop(heap)
        visited.add(current_node)

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                if neighbor not in visited:
                    heapq.heappush(heap, (distance, neighbor))

    return distances


graph = {
    'A': [('B', 5), ('C', 3), ('D', 6), ('G', 1), ('H', 0)],
    'B': [('C', 6), ('E', 4)],
    'C': [('E', 6), ('D', 7)],
    'D': [('F', 2), ('E', 2)],
    'E': [('G', 3), ('F', 4)],
    'F': [('G', 5)],
    'G': [],
    'H': [('D', 1)]
}

graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('D', 5), ('E', 10)],
    'C': [('F', 8), ('E', 1)],
    'D': [('G', 6)],
    'E': [('D', 3), ('H', 2)],
    'F': [('E', 5), ('I', 4)],
    'G': [('J', 2)],
    'H': [('G', 1), ('K', 3)],
    'I': [('H', 1), ('L', 7)],
    'J': [('M', 4)],
    'K': [('J', 2), ('N', 6)],
    'L': [('K', 2), ('O', 5)],
    'M': [('O', 3)],
    'N': [('M', 1)],
    'O': []
}


print('Version 1:', dijkstra_v1(graph, 'A'))
print('Version 2:', dijkstra_v2(graph, 'A'))
