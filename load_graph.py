from collections import deque 

def load_file(file_name):
    tasks = dict()

    with open(file_name) as f:
        for line in f:
            # CÓDIGO_PROCESO,COSTO_EQUIPO1,COSTO_EQUIPO2,[LISTA DE DEPENDENCIAS CON SUS COSTOS]
            tokens = line.rstrip().split(",")
            id = tokens[0]
            cost_a = int(tokens[1])
            cost_b = int(tokens[2])
            dependencies = []
            for i in range(3, len(tokens)-1, 2):
                dep = tokens[i]
                dep_cost = int(tokens[i+1])
                dependencies.append((dep, dep_cost))

            tasks[id] = (cost_a, cost_b, dependencies)

    return tasks


def create_graph(tasks):
    visited = set()
    costs = dict()
    capacity = dict()

    costs['s'] = dict()
    costs['t'] = dict()

    for id in tasks.keys():
        if id not in visited:
            # para cada nodo no visitado agregar todos los nodos del grafo de dependencias
            costs['s'][id] = 0 
            visited.add(id)
            cost_a, cost_b, dependencies = tasks[id]
            costs[id] = {'A'+id: cost_a, 'B'+id: cost_b}
            costs['A'+id] = dict()
            costs['B'+id] = dict()

            queue = deque(dependencies)
            while len(queue) > 0:
                id_dep, dep_cost = queue.popleft()
                visited.add(id_dep)
                cost_a, cost_b, dependencies = tasks[id_dep]

                costs['A'+id]['A'+id_dep] = cost_a
                costs['A'+id]['B'+id_dep] = cost_b+dep_cost
                costs['B'+id]['A'+id_dep] = cost_a+dep_cost
                costs['B'+id]['B'+id_dep] = cost_b

                costs['A'+id_dep] = dict()
                costs['B'+id_dep] = dict()

                # agregar dependencias siguientes
                for dep in dependencies:
                    if dep[0] not in visited:
                        queue.append(dep)

                # agregar dependencias previas
                for id_task, (cost_a, cost_b, dependencies) in tasks.items():
                    if id_task not in visited:
                        for id_dep_prev, cost in dependencies:
                            if id_dep_prev == id_dep:
                                queue.append((id_task, cost))
                id = id_dep

            costs['A'+id]['t'] = 0
            costs['B'+id]['t'] = 0
            

    # crear grafo residual de capacidades
    for id in costs.keys():
        capacity[id] = dict()

    for id, dependencies in costs.items():
        for dep_id in dependencies.keys():
            capacity[id][dep_id] = 1
            capacity[dep_id][id] = 0

    return capacity, costs

def load_graph(file_name):
    tasks = load_file(file_name)
    return create_graph(tasks)