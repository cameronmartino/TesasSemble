class Node:
    def __init__(self, data):
        self.data = data
        self.in_edges = []
        self.out_edges = []

    def __str__(self):
        return str(self.data)

    __repr__ = __str__

    def append_in_edges(self, edges):
        if isinstance(edges, list):
            for edge in edges:
                self.in_edges.append(edge)
        elif edges is not None:
            self.in_edges.append(edges)

    def append_out_edges(self, edges):
        if isinstance(edges, list):
            for edge in edges:
                self.out_edges.append(edge)
        elif edges is not None:
            self.out_edges.append(edges)

    def remove_in_edges(self, edges):
        if isinstance(edges, list):
            for edge in edges:
                if edge in self.in_edges:
                    self.in_edges.remove(edge)
                    # Add code to remove node from Edge class
                    # Add this only if you control edges from nodes, otherwise
                    # use 'remove_connection' from an edge
        elif edges is not None:
            if edges in self.in_edges:
                self.in_edges.remove(edges)
                # Add code to remove node from Edge class
                # Add this only if you control edges from nodes, otherwise use
                # 'remove_connection' from an edge

    def remove_out_edges(self, edges):
        if isinstance(edges, list):
            for edge in edges:
                if edge in self.out_edges:
                    self.out_edges.remove(edge)
                    # Add code to remove node from Edge class
                    # Add this only if you control edges from nodes, otherwise
                    # use 'remove_connection' from an edge
        elif edges is not None:
            if edges in self.out_edges:
                self.out_edges.remove(edges)
                # Add code to remove node from Edge class
                # Add this only if you control edges from nodes, otherwise use
                # 'remove_connection' from an edge

    def print_out_connections(self):
        connections = ''
        count = 0
        for edge in self.out_edges:
            if count == 0:
                connections += edge.node_b.__str__()
            else:
                connections += ',' + edge.node_b.__str__()
            count += 1
        if len(connections) > 0:
            print(self, '->', connections)

    def get_data(self):
        return self.data

    def in_degree(self):
        return len(self.in_edges)

    def out_degree(self):
        return len(self.out_edges)


class Edge:
    def __init__(self, data, node_a=None, node_b=None):
        self.data = data
        self.node_a = node_a
        self.node_b = node_b
        if self.node_a is not None and self.node_b is not None:
            self.node_b.append_in_edges(self)
            self.node_a.append_out_edges(self)

    def __str__(self):
        return str(self.data)

    __repr__ = __str__

    def set_node_a(self, node_a):
        old_a = self.node_a
        self.node_a = node_a
        if self.node_b is not None:
            self.node_a.append_out_edges(self)
            if self not in self.node_b.in_edges:
                self.node_b.append_in_edges(self)
            if old_a is not None:
                old_a.remove_out_edges(self)

    def set_node_b(self, node_b):
        old_b = self.node_b
        self.node_b = node_b
        if self.node_a is not None:
            self.node_b.append_in_edges(self)
            if self not in self.node_a.out_edges:
                self.node_b.append_out_edges(self)
            if old_b is not None:
                old_b.remove_in_edges(self)

    def remove_connection(self):
        if self.node_a is not None and self.node_b is not None:
            self.node_a.remove_out_edges(self)
            self.node_b.remove_in_edges(self)
            self.data = 'EmptyEdge'

    def print_connection(self):
        if self.node_a is not None and self.node_b is not None:
            print(self.node_a, '->', self.node_b)
        elif self.node_a is not None:
            print(self.node_a, '->')
        elif self.node_b is not None:
            print('->', self.node_b)
        else:
            pass

    def get_data(self):
        return self.data


def graph_deep_copy(nodes, edges):
    '''
    This function performs a deep copy of a graph. This is made to clone the graph using new instances for
    Node and Edge. This is useful when modifying the graph temporally.

    Parameters
    __________

    nodes : dict
        A dictionary where each key is a str and each value is a Node instance.

    edges : array-like
        A list of Edge instances that represent the connections among the Node instances in nodes.

    Returns
    _______

    new_nodes : dict
        A dictionary where each key is a str and each value is a Node instance. This corresponds to a deep copy of nodes.

    new_edges : array-like
        A list of Edge instances that represent the connections among the Node instances in new_nodes. This corresponds
        to a deep copy of edges, but referencing to nodes in new_nodes.
    '''
    # Create new instances
    new_nodes = {}
    new_edges = []

    # Node instances
    for node in nodes.values():
        new_nodes[str(node)] = Node(node.data)

    # Edge instances
    for edge in edges:
        new_edges.append(Edge(edge.data,
                              node_a=new_nodes[str(edge.node_a)],
                              node_b=new_nodes[str(edge.node_b)]))

    return new_nodes, new_edges
