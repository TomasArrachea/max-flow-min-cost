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


def compute_graph_size(tasks):
    vertices = 2
    for id, (cost_a, cost_b, dependencies) in tasks.items():
        vertices += 3
        for dep, dep_cost in dependencies:
            vertices -= 1
    return vertices


def get_independent_tasks(tasks):
    independents = dict()
    for id, (cost_a, cost_b, dependencies) in tasks.items():
        independents[id] = True

    for id, (cost_a, cost_b, dependencies) in tasks.items():
        for dep, dep_cost in dependencies:
            independents[dep] = False
    return independents


def create_graph(tasks):
    independents = get_independent_tasks(tasks)
    costs = dict(); capacity = dict()

    # agregar nodos iniciales
    costs["s"] = dict() # no pueden venir tasks con ese id
    for id, idpt in independents.items():
        if idpt == True:
            costs['s'][id] = 0 # cada nodo guarda una lista de tuplas con los nodos que apunta y con que costo, NO CAPACIDAD porque en todos vale 1

    # agregar nodos para tareas dependientes
    for id in costs['s'].keys(): # para las tareas iniciales t1 y t4
        cost_a, cost_b, dependencies = tasks[id]
        costs[id] = {'A'+id: cost_a, 'B'+id: cost_b}

        costs['A'+id] = dict()
        costs['B'+id] = dict()

        # ir encolando las dependencias de los nodos y se van poniendo una atras de la otra
        queue = dependencies        
        while len(queue) > 0:
            id_dep, dep_cost = queue.pop(0)
            cost_a, cost_b, dependencies = tasks[id_dep]
            costs['A'+id]['A'+id_dep] = cost_a
            costs['A'+id]['B'+id_dep] = cost_b+dep_cost
            costs['B'+id]['A'+id_dep] = cost_a+dep_cost
            costs['B'+id]['B'+id_dep] = cost_b

            costs['A'+id_dep] = dict()
            costs['B'+id_dep] = dict()
            queue.extend(dependencies)
            id = id_dep

    # agregar nodo final
    for id, dependencies in costs.items():
        if len(dependencies) == 0:
            dependencies['t'] = 0
    costs['t'] = dict()

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