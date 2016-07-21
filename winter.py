from collections import defaultdict, deque
# n = increment to be applied on alpha
# m = no. of edges  
class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.d1 = {}
        self.d2 = {}
        self.m1 = 0
 
    def add_node(self, value):
        self.nodes.add(value)
        self.m1 += 1
 
    def add_edge(self, from_node, to_node, distance, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.d1[(from_node, to_node)] = distance
        self.d2[(from_node, to_node)] = weight
 
    def combined_weight(self, min_node, edge, alpha):
        d = alpha*self.d1[(min_node, edge)] + (1-alpha)*self.d2[(min_node, edge)]
        return d
 
    def get_m(self):
        return self.m1
 
def dijkstra(graph, initial, dest, alpha):
    visited = {initial: 0}
    limits = {initial: 0}
    path = {}
 
    nodes = set(graph.nodes)
 
    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break
 
        nodes.remove(min_node)
        current_weight = visited[min_node] 
        current_limit = limits[min_node]
 
        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.combined_weight(min_node, edge, alpha)
                lim = current_limit + graph.combined_weight(min_node, edge, 0)
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node
                limits[edge] = lim
 
    return visited, path, limits[dest]
 
def short_path(graph, origin, destination, limit, n):
    alpha = 1.0
    visited = {}
    paths = {}
 
    m = graph.get_m()
 
    visited, paths, lim = dijkstra(graph, origin, destination, alpha)
    if (lim <= limit):
        print "1"
        return visited, paths, lim
    else:
        alpha = 0.0
        visited, paths, lim = dijkstra(graph, origin, destination, alpha)
        if (lim > limit):
            print "No possible path"
            return visited, paths, lim
        elif (lim == limit):
            print "3"
            return visited, paths, lim
        else:
            u = 0
            v = 1
            i = 1
            k = 1
            while True:
                diff = (v-u)/n
                while True:
                    alpha = u + k*diff
                    visited, paths, lim = dijkstra(graph, origin, destination, alpha)
                    if (lim == limit):
                        print i
                        print "4"
                        return visited, paths, lim
                    elif(lim < limit):
                        u = alpha
                        if (k == n-1):
                            break
                    else:
                        v = alpha
                        break
                    k += 1
                i += 1
                if (i > m):
                    break
    print ('No of iterations :',i + 1)
    return visited, paths, lim
 
 
def print_out(graph, origin, destination, limit, n):
    visited, paths, lim = short_path(graph, origin, destination, limit, n)
    full_path = deque()
    _destination = paths[destination]
 
    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]
 
    full_path.appendleft(origin)
    full_path.append(destination)
 
    return visited[destination], lim, list(full_path)
 
# if __name__ == '__main__':
#     graph = Graph()
 
#     for node in ['00', '01', '02', '10', '11', '12', '20', '21', '22', '30', '31', '32']:
#         graph.add_node(node)
 
#     graph.add_edge('00', '01', 333.3, 30)
#     graph.add_edge('00', '10', 166.7, 60)
#     graph.add_edge('01', '02', 250, 40)
#     graph.add_edge('01', '11', 83.3, 120)
#     graph.add_edge('02', '12', 55.5, 180)
#     graph.add_edge('10', '11', 166.7, 60)
#     graph.add_edge('10', '20', 142.9, 70)
#     graph.add_edge('11', '12', 142.9, 70)    
#     graph.add_edge('12', '22', 52.6, 19)
#     graph.add_edge('20', '21', 111.1, 9)
#     graph.add_edge('20', '30', 125.0, 8)
#     graph.add_edge('21', '22', 100.0, 10)
#     graph.add_edge('21', '31', 71.4, 14)
#     graph.add_edge('22', '32', 50.0, 20)
#     graph.add_edge('30', '31', 83.3, 12)
#     graph.add_edge('31', '32', 76.9, 13)
#     # sending the graph along with starting and end nodes
#     print(print_out(graph, '00', '32', 165, 3))
 