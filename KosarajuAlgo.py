from collections import defaultdict

def kosaraju(graph):
    def dfs(graph, node, stack):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(graph, neighbor, stack)
        stack.append(node)

    def dfs_reverse(graph, node, scc):
        visited.add(node)
        scc.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_reverse(graph, neighbor, scc)

    stack = []
    visited = set()
    for node in graph:
        if node not in visited:
            dfs(graph, node, stack)

    reversed_graph = defaultdict(list)
    for u in graph:
        for v in graph[u]:
            reversed_graph[v].append(u)

    visited.clear()
    scc_list = []
    while stack:
        node = stack.pop()
        if node not in visited:
            scc = set()
            dfs_reverse(reversed_graph, node, scc)
            scc_list.append(scc)

    return scc_list

graph = {1: [2], 2: [3, 4], 3: [1], 4: [5], 5: [4]}
print(kosaraju(graph))
