import networkx as nx

class GeneticNetwork(nx.DiGraph):
    def __init__(self, regulators=None, tus=None):
        super().__init__()
        if tus:
            self.add_nodes_from(tus)
        if regulators:
            self.add_edges_from(regulators)

    def add_tu(self, tu):
        self.add_node(tu)

    def add_regulator(self, from_TU, to_TU, regulator):
        self.add_edge(from_TU, to_TU, object=regulator)

    def step(self, circuit, growth_rate=1, dt=0.1):
        for r1,r2,data in circuit.nodes.data():
            tu = data['object']
            expression_rate = tu.output(r1.concentration, dt)
            r2.step(expression_rate, growth_rate, dt)
        for r in circuit.edges:
            r.update()



        
