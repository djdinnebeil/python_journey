import heapq

def dijkstra_bugs(graph, start):
    distances = {node: float('infinity') for node in range(20)}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    all_nodes_visited = len(distances) == 20

    return distances, all_nodes_visited

graph = {
    1: [(2, 1), (3, 4)],
    2: [(3, 2), (4, 5)],
    3: [(4, 1)],
    4: []
}

print(dijkstra_bugs(graph, 1))
print(dijkstra_bugs(graph, 4))