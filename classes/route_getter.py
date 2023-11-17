
from dijkstar import *

class RouteGetter:
    def __init__(self):
        self.table = {
            "device_1": 9001,
            "device_2": 9002,
            "device_3": 9003,
            "device_4": 9004,
            "device_5": 9005,
        }
        self.graph = Graph(undirected=True)
        self.graph.add_edge("device_1", "device_2", 1)
        self.graph.add_edge("device_1", "device_5", 1)
        self.graph.add_edge("device_2", "device_4", 1)
        self.graph.add_edge("device_2", "device_3", 1)
        self.graph.add_edge("device_4", "device_5", 1)

    def get_next_hop(self, source, destination):
        path = find_path(self.graph, source, destination)
        next_hop = ""
        try:
            if len(path.nodes) > 1:
                next_hop = path.nodes[1]
            else:
                next_hop = source
            return (next_hop, self.table[next_hop])
        except KeyError:
            print(next_hop, self.table)
            return 

    def remove_from_graph(self, device):
        self.graph.remove_node(device)
    
    def keys(self, id):
        list = self.table
        list.get(id)
        return list.keys()

