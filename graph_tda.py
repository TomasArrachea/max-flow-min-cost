def max_flow_ford_fulkerson(graph, names):
    # Create a residual graph and fill the residual graph with
    # given capacities in the original graph as residual capacities
    # in residual graph
    res_graph = [[0 for i in range(len(graph))]
                 for j in range(len(graph))]

    for u in range(len(graph)):
        for v in range(len(graph)):
            res_graph[u][v] = graph[u][v]

    # This array is filled by BFS and to store path
    path = [None] * len(graph)

    # Augment the flow while tere is path from source to sink
    max_flow = 0
    condition, array = bfs(res_graph, 0, len(graph)-1, path)
    while condition:
        # Find minimum residual capacity of the edges along the
        # path filled by BFS. Or we can say find the maximum flow
        # through the path found.
        path_flow = float("Inf")
        s = len(graph)-1
        while s != 0:
            path_flow = min(path_flow, res_graph[path[s]][s])
            s = path[s]

        # Add path flow to overall flow
        max_flow += path_flow

        # update residual capacities of the edges and reverse edges
        # along the path
        v = len(graph)-1
        while v != 0:
            u = path[v]
            res_graph[u][v] -= path_flow
            res_graph[v][u] += path_flow
            v = path[v]
        condition, array = bfs(res_graph, 0, len(graph)-1, path)
    team_a_tasks, team_b_tasks = get_tasks(array, names)
    return max_flow, team_a_tasks, team_b_tasks


def get_tasks(array, names):
    team_a = []
    team_b = []
    for i in range(len(array)):
        if ((i == 0) | (i == len(array) - 1)):
            continue
        if array[i] == True:
            team_b.append(names[i])
        if array[i] == False:
            team_a.append(names[i])
    return team_a, team_b


# Returns true if there is a path from source 's' to sink 't' in
# residual graph. Also fills parent[] to store the path


def bfs(res_graph, s, t, parent):

    # Mark all the vertices as not visited
    visited = [False]*(len(res_graph))

    # Create a queue for BFS
    queue = []

    # Mark the source node as visited and enqueue it
    queue.append(s)
    visited[s] = True

    # Standard BFS Loop
    while queue:

        # Dequeue a vertex from queue
        u = queue.pop(0)

        # Get all adjacent vertices of the dequeued vertex u
        # If a adjacent has not been visited, then mark it
        # visited and enqueue it
        for ind, val in enumerate(res_graph[u]):
            if visited[ind] == False and val > 0:
                queue.append(ind)
                visited[ind] = True
                parent[ind] = u

    # If we reached sink in BFS starting from source, then return
    # true, else false
    return (visited[t], visited)


def load_graph(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    cont = 1
    size = len(lines)
    graph = [[0 for i in range(size+2)]
             for j in range(size+2)]
    nombres = [0 for i in range(size+2)]
    graph_size = len(graph)
    indices = {}
    for i in lines:
        elements = i.split(",")
        nombres[cont] = elements[0]
        indices[elements[0]] = cont
        cont = cont + 1
    cont = 1
    for i in lines:
        i.replace("\n", "")
        elements = i.split(",")
        elements[-1] = elements[-1].replace("\n", "")
        idx = indices[elements[0]]
        graph[0][cont] = int(elements[1])  # Costo equipo 1
        graph[cont][graph_size - 1] = int(elements[2])  # Costo equipo 2
        dependencies = elements[3:]
        cont = cont + 1
        cont_dep = 0
        while (cont_dep < len(dependencies)):
            idx_dependency = indices[dependencies[cont_dep]]
            graph[idx][idx_dependency] = int(dependencies[cont_dep + 1])
            graph[idx_dependency][idx] = int(dependencies[cont_dep + 1])
            cont_dep = cont_dep + 2

    # for i in graph:
        # print(i)
    return graph, nombres


# graph = build_graph()
# max_flow, bfs_t = max_flow_ford_fulkerson(graph)
# print("max_flow ", max_flow)
# print(bfs_t)
