#global gt
import graph_tool.all as gt
import time


class GraphGT(object):

    @staticmethod
    def compare(G1, G2):
        raise NotImplementedError

    @staticmethod
    def compare_nodes(n1, n2):
        raise NotImplementedError

    @staticmethod
    def compare_edges():
        raise NotImplementedError

    def __init__(self, G=None, Type=None):

        # unused maxVert

        self.maxVertices = 0

        # create a Di-graph if not created already

        if G is None:
            self.G = gt.Graph()
            self.Type = 'test_no'
        else:
            self.G = G
            self.Type = Type

        self.node_vertex_dict = {}
        self.edge_attr_dict = self.G.new_edge_property('object')

    def check_n_add_n_get(self, n):
        v = self.node_vertex_dict.get(n)

        # if node does not exist in the graph

        if v is None:

            # allocate a new vertex

            v = self.G.add_vertex()

            # add it to the dictionary for future

            self.node_vertex_dict[n] = v
        return v

    def nodes(self):

        # why is this needed?

        raise NotImplementedError

    def add_edge(
        self,
        n1,
        n2,
        attr_val=None,
        ):
        v1 = self.check_n_add_n_get(n1)
        v2 = self.check_n_add_n_get(n2)

        e = self.G.add_edge(v1, v2)
        self.edge_attr_dict[e] = attr_val

    def add_edge_wt(
        self,
        v1,
        v2,
        weight,
        ):
        raise NotImplementedError
        self.G.add_edge(v1, v2, w=weight)

    def add_node(self, n):
        raise NotImplementedError  # Actually, its just not tested...
        self.check_n_add_n_get(n)
        return

############################## UNFINISHED FROM HERE

    def get_path_attr_list(self, path):
        raise NotImplementedError
        attr_list = []
        for (v1, v2) in U.pairwise(path):
            attr_list.append(self.G[v1][v2]['attr'])
        return attr_list

    # Actually draws the graph!! Need to rewrite get_path_generator() from
    # scratch for gt. Also, destroys the passed in graph (oops) :D
    # Hence, use this function only for debugging!!
    # # TODO: Fix it, of course?

    def get_path_generator(
        self,
        source_list,
        sink_list,
        max_depth=None,
        ):

        print 'WARNING: This is actually a plotting function!!!'

        num_source_nodes = len(source_list)
        num_sink_nodes = len(sink_list)

        # super_source_vertex = g.add_vertex()
        # super_sink_vertex = g.add_vertex()

        super_source_vertex = 'super_source_vertex'
        super_sink_vertex = 'super_sink_vertex'

        edge_list = zip([super_source_vertex] * num_source_nodes, source_list)
        for e in edge_list:
            self.add_edge(*e)

        edge_list = zip(sink_list, [super_sink_vertex] * num_sink_nodes)
        for e in edge_list:
            self.add_edge(*e)

        g = self.G

        pos = gt.arf_layout(g, max_iter=0)
        gt.graph_draw(g, pos=pos, vertex_text=self.G.vertex_index)
        time.sleep(1000)
        exit()

        gt.graph_draw(self.G, vertex_text=self.G.vertex_index)
        time.sleep(1000)

#        print edge_list

        # Add edges:
        #   \forall sink \in sink_list. sink -> super sink node

        edge_list = zip(sink_list, [dummy_super_sink_node] * num_sink_nodes)
        H.add_edges_from(edge_list)

#        print edge_list

#        print '='*80
        # TODO: WHY?
        # Switching this on with def path_gen(), results in empty path and no further results!!
        # #xplanation required!
#        for path in nx.all_simple_paths(H, dummy_super_source_node, dummy_super_sink_node):
#            print path
#        print '='*80

        # TODO: how to do this with lambda?
        # Also, is this indeed correct?

        def path_gen():
            for i in nx.all_simple_paths(H, dummy_super_source_node,
                    dummy_super_sink_node):

                # Remove the first (super source)
                # and the last element (super sink)

                yield i[1:-1]

        # return lambda: [yield i[1:-1] for i in nx.all_simple_paths(H,
        # dummy_super_source_node, dummy_super_sink_node)]

        return path_gen()

    def neighbors(self, node):
        raise NotImplementedError
        return self.G.neighbors(node)

    def draw(self, pos_dict=None):
        raise NotImplementedError
        nx.draw_networkx(self.G, pos=pos_dict, labels=pos_dict,
                         with_labels=True)

    def __contains__(self, key):
        raise NotImplementedError
        return key in self.G

    def __repr__(self):
        raise NotImplementedError
        s = ''
        s += '''==== Nodes ==== {} '''.format(self.G.nodes())
        s += '''==== Edges ==== {} '''.format(self.G.edges())
        return s
