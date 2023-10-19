import random

def min_cut(graph):
    while len(graph) > 2:
        u, v = random.choice(graph)
        graph.remove((u, v))
        new_vertex = u + v

        # Merge vertices connected to u and v
        for vertex in graph:
            if u in vertex:
                vertex.remove(u)
            if v in vertex:
                vertex.remove(v)
            if new_vertex not in vertex:
                vertex.append(new_vertex)

    return len(graph[0])  # The size of the final cut

graph = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)]
print(min_cut(graph))
