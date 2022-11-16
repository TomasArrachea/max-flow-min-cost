import heapq


class Graph:

    def __init__(self, capacity_graph, cost_graph):
        self.capacity_graph = capacity_graph
        self.cost_graph = cost_graph
        self.size = len(capacity_graph)


    def dijkstra(self, s, t, parent):

        for id in parent.keys():
            parent[id] = None  # almacena desde donde se visita cada nodo para recuperar el camino final

        cost_visited = dict()

        heap = []
        heapq.heappush(heap, (0, s))
        cost_visited[s] = 0

        while heap:

            cur_cost, cur_node = heapq.heappop(heap)

            if cur_node == t:
                break

            for id, capacity in self.capacity_graph[cur_node].items():
                if capacity > 0:

                    neigh_cost = self.cost_graph[cur_node][id]
                    new_cost = cost_visited[cur_node] + neigh_cost

                    if id not in cost_visited or new_cost < cost_visited[id]:
                        heapq.heappush(heap, (new_cost, id))
                        cost_visited[id] = new_cost
                        parent[id] = cur_node

        # Devolver si se visito el nodo final o no
        return parent[t] != None


    def FordFulkerson(self, source='s', sink='t'):

        parent = dict()
        team_A_tasks = []
        team_B_tasks = []
        max_cost = 0

        # Aumentar el flujo mientras haya nuevos caminos de la fuente al sumidero
        while self.dijkstra(source, sink, parent):
            # Buscar el cuello de botella del camino
            path_flow = float("inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, self.capacity_graph[parent[s]][s])
                s = parent[s]

            # Aumentar el camino
            v = sink
            while (v != source):
                if v.startswith("A"):
                    team_A_tasks.append(v[1:])
                if v.startswith("B"):
                    team_B_tasks.append(v[1:])
                u = parent[v]
                self.capacity_graph[u][v] -= path_flow
                self.capacity_graph[v][u] += path_flow
                max_cost += path_flow * self.cost_graph[u][v]
                v = parent[v]

        return max_cost, team_A_tasks, team_B_tasks