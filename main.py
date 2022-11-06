from graph import Graph
from load_graph import load_graph
import getopt
import sys 


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hf:l:b:", ["help", "file=", "length=", "boxes="])
    except getopt.GetoptError:
        sys.exit(2)

    file_name = "procesos.txt"

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("Optional arguments")
            print("  -h, --help     list of arguments")
            print("  -f, --file     file name")
            
            return
        elif opt in ("-f", "--file"):
            file_name = arg

    capacity_graph, cost_graph = load_graph(file_name)

    g = Graph(capacity_graph, cost_graph)
    max_cost, team_A_tasks, team_B_tasks = g.FordFulkerson()
    
    print(f"El costo total es {max_cost}")
    print(f"El equipo A debe realizar las tareas {team_A_tasks}")
    print(f"El equipo B debe realizar las tareas {team_B_tasks}")
    

if __name__ == "__main__":
    main(sys.argv[1:])