#!/usr/bin/python
# -*- coding: utf-8 -*-

import err
import utils as U

# needed for testing

import random as rand
import time

#  FIX heap duplicates used by different ksp!

import heapq
from heapq import heappush, heappop

from itertools import count
from collections import defaultdict

from blessings import Terminal
term = Terminal()


def graph_factory(graph_type):
    if graph_type == 'nx':
        global nx
        import networkx as nx
        return GraphNX()
    elif graph_type == 'gt':
        global gt
        import graph_tool.all as gt
        return GraphGT()
    else:
        raise err.Fatal('unknown graph library requested: {}'.format(graph_type))


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


class GraphNX(object):

    @staticmethod
    def compare(G1, G2):
        G1 = G1.G
        G2 = G2.G

        G1_nodes_set = set(G1.nodes())
        G2_nodes_set = set(G2.nodes())

        G1_edges_set = set(G1.edges())
        G2_edges_set = set(G2.edges())

        G1_in_G2_nodes = G1_nodes_set.issubset(G2_nodes_set)
        G2_in_G1_nodes = G2_nodes_set.issubset(G1_nodes_set)

        G1_in_G2_edges = G1_edges_set.issubset(G2_edges_set)
        G2_in_G1_edges = G2_edges_set.issubset(G1_edges_set)

        G1_in_G2 = G1_in_G2_nodes and G1_in_G2_edges
        G2_in_G1 = G2_in_G1_nodes and G2_in_G1_edges

        print 'G1_in_G2_nodes: {}, G1_in_G2_edges: {}'.format(G1_in_G2_nodes,
                G1_in_G2_edges)
        print 'G2_in_G1_nodes: {}, G2_in_G1_edges: {}'.format(G2_in_G1_nodes,
                G2_in_G1_edges)

        print '''G1_nodes_set - G2_nodes_set
{}
'''.format(G1_nodes_set
                - G2_nodes_set)

        G1_and_G2_are_equal = G1_in_G2 and G2_in_G1

        print 'G1_in_G2: {}, G2_in_G1: {}\n'.format(G1_in_G2, G2_in_G1)

        return G1_and_G2_are_equal

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

            self.G = nx.DiGraph()
            self.Type = 'test_no'
        else:
            self.G = G
            self.Type = Type

    def nodes(self):
        return self.G.nodes()

    def add_edge(
        self,
        v1,
        v2,
        ci=None,
        pi=None,
        weight=1,
        ):
        self.G.add_edge(v1, v2, weight=1, ci=ci, pi=pi)

    def add_edges_from(
        self,
        edge_list,
        ci=None,
        pi=None,
        weight=1,
        ):
        self.G.add_edges_from(edge_list, weight=1, ci=ci, pi=pi)

    def add_node(self, v):
        self.G.add_node(v)

    def get_path_attr_list(self, path, attrs):
        attr_map = defaultdict(list)
        for (v1, v2) in U.pairwise(path):
            for attr in attrs:
                attr_map[attr].append(self.G[v1][v2][attr])
        return attr_map

    # ###################### KSP 1 ##################################################
    # https://gist.github.com/guilhermemm/d4623c574d4bccb6bf0c
    # __author__ = 'Guilherme Maia <guilhermemm@gmail.com>'
    # __all__ = ['k_shortest_paths']

    def k_shortest_paths(
        self,
        G,
        source,
        target,
        k=1,
        weight='weight',
        ):
        """Returns the k-shortest paths from source to target in a weighted graph G.

        Parameters
        ----------
        G : NetworkX graph

        source : node
           Starting node

        target : node
           Ending node

        k : integer, optional (default=1)
            The number of shortest paths to find

        weight: string, optional (default='weight')
           Edge data key corresponding to the edge weight

        Returns
        -------
        lengths, paths : lists
           Returns a tuple with two lists.
           The first list stores the length of each k-shortest path.
           The second list stores each k-shortest path.

        Raises
        ------
        NetworkXNoPath
           If no path exists between source and target.

        Examples
        --------
        >>> G=nx.complete_graph(5)
        >>> print(k_shortest_paths(G, 0, 4, 4))
        ([1, 2, 2, 2], [[0, 4], [0, 1, 4], [0, 2, 4], [0, 3, 4]])

        Notes
        ------
        Edge weight attributes must be numerical and non-negative.
        Distances are calculated as sums of weighted edges traversed.

        """

        if source == target:
            return ([0], [[source]])

        (length, path) = nx.single_source_dijkstra(G, source, target,
                weight=weight)
        if target not in length:
            raise nx.NetworkXNoPath('node %s not reachable from %s' % (source,
                                    target))

        lengths = [length[target]]
        paths = [path[target]]
        c = count()
        B = []

        # Is deep copy really required?
        #   Fails due to embedded Ctype objects which can not be pickled
        # # G_original = G.copy()
        # Swapping with shallow copy...will it work?

        G_original = G
        if nx.is_directed(G_original):
            G = nx.DiGraph(G_original)
        else:
            G = nx.Graph(G_original)

        ######################################
        #TODO: wrap this up somehow
        print ''
        print term.move_up + term.move_up
        ######################################
        print 'getting K:{} paths...'.format(k),
        for i in range(1, k):
            with term.location():
                print i
            for j in range(len(paths[-1]) - 1):
                spur_node = paths[-1][j]
                root_path = (paths[-1])[:j + 1]

                edges_removed = []
                for c_path in paths:
                    if len(c_path) > j and root_path == c_path[:j + 1]:
                        u = c_path[j]
                        v = c_path[j + 1]
                        if G.has_edge(u, v):
                            edge_attr = G.edge[u][v]
                            G.remove_edge(u, v)
                            edges_removed.append((u, v, edge_attr))

                for n in range(len(root_path) - 1):
                    node = root_path[n]

                    # out-edges

                    for (u, v, edge_attr) in G.edges_iter(node, data=True):

                        # print 'lala1: {} -> {}'.format(u,v)

                        G.remove_edge(u, v)
                        edges_removed.append((u, v, edge_attr))

                    if G.is_directed():

                        # in-edges

                        for (u, v, edge_attr) in G.in_edges_iter(node,
                                data=True):

                            # print 'lala2: {} -> {}'.format(u,v)

                            G.remove_edge(u, v)
                            edges_removed.append((u, v, edge_attr))

                (spur_path_length, spur_path) = nx.single_source_dijkstra(G,
                        spur_node, target, weight=weight)
                if target in spur_path and spur_path[target]:
                    total_path = root_path[:-1] + spur_path[target]
                    total_path_length = self.get_path_length(G_original,
                            root_path, weight) + spur_path_length[target]
                    heappush(B, (total_path_length, next(c), total_path))

                for e in edges_removed:
                    (u, v, edge_attr) = e
                    G.add_edge(u, v, edge_attr)

            if B:
                (l, _, p) = heappop(B)
                lengths.append(l)
                paths.append(p)
            else:
                break

        return (lengths, paths)

    def get_path_length(
        self,
        G,
        path,
        weight='weight',
        ):
        length = 0
        if len(path) > 1:
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]

                length += G.edge[u][v].get(weight, 1)

        return length

    # ################################### KSP2 ###########################
    # ######################## GREG BERNSTEIN #######################
    # https://groups.google.com/forum/#!topic/networkx-discuss/0niVmZZXxGA

    def ksp_gregBern(
        self,
        G,
        source,
        target,
        k=1,
        weight='weight',
        ):
        YKSP = YenKShortestPaths(G, weight)
        path_list = []

        wp0 = YKSP.findFirstShortestPath(source, target)
        p0 = wp0.nodeList
        path_list.append(p0)

        print 'getting K:{} paths...'.format(k)
        for i in range(k):
            wpi = YKSP.getNextShortestPath()
            if wpi is None:
                break
            pi = wpi.nodeList
            path_list.append(pi)
            print i, ' '

        # print path_list

        return path_list

    # ################################### KSP END ###########################

    def get_path_generator(
            self,
            source_list,
            sink_list,
            max_depth,
            max_paths
            ):

        # Create a shallow copy of the graph

        H = nx.DiGraph(self.G)

        # All modifications are now done on this shallow copy H

        # Define super source and sink nodes
        # A Super source node has a directed edge to each source node in the
        # source_list
        # Similarily, a Super sink node has a directed edge from each sink node
        # in the sink_list

        dummy_super_source_node = 'source'
        dummy_super_sink_node = 'sink'
        num_source_nodes = len(source_list)
        num_sink_nodes = len(sink_list)

        # increment max_depth by 2 to accommodate edges from 'super source' and
        # to 'super sink'
        max_depth += 2

        # Add edges:
        #   \forall source \in source_list. super source node -> source

        edge_list = zip([dummy_super_source_node] * num_source_nodes,
                        source_list)
        H.add_edges_from(edge_list, weight=1)

#        print edge_list

        # Add edges:
        #   \forall sink \in sink_list. sink -> super sink node

        edge_list = zip(sink_list, [dummy_super_sink_node] * num_sink_nodes)
        H.add_edges_from(edge_list, weight=1)

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

            # all_shortest_paths
            # all_simple_paths
            #

            #K = 100
            K = max_paths
            (len_list, path_list) = self.k_shortest_paths(H,
                                                          dummy_super_source_node,
                                                          dummy_super_sink_node,
                                                          k=K)

            # path_list = self.ksp_gregBern(H, dummy_super_source_node,
            #                                              dummy_super_sink_node,
            #                                              k=K)

            # using simple paths
            # for i in nx.all_simple_paths(H, dummy_super_source_node,
            #                             dummy_super_sink_node,
            #                             cutoff=max_depth):

            # using all sohrtest paths
            # for i in nx.all_shortest_paths(H, dummy_super_source_node, dummy_super_sink_node):
                # Remove the first (super source)
                # and the last element (super sink)

            for p in path_list:
                l = len(p)
                #print l, max_depth
                if l <= max_depth:
                    yield p[1:-1]

        # return lambda: [yield i[1:-1] for i in nx.all_simple_paths(H,
        # dummy_super_source_node, dummy_super_sink_node)]

        return path_gen()

    def neighbors(self, node):
        return self.G.neighbors(node)

    def draw(self, pos_dict=None):
        nx.draw_networkx(self.G, pos=pos_dict, labels=pos_dict,
                         with_labels=True)

    def __contains__(self, key):
        return key in self.G

    def __repr__(self):
        s = ''
        s += '''==== Nodes ==== {} '''.format(self.G.nodes())
        s += '''==== Edges ==== {} '''.format(self.G.edges())
        return s


def random_graph(
    num_nodes,
    num_edges,
    dim,
    seed=None,
    directed=False,
    ):

    raise NotImplementedError('modify to work with new abstraction object')
    G = nx.gnm_random_graph(num_nodes, num_edges, seed, directed)
    abstract_G = nx.DiGraph()

    # create a mapping from G to abstract_G

    graph_map = {}

    # innane pos_dict for plotting only

    pos_dict = {}

    # create the nodes of abstract_G

    N_MAX = 5
    for n in G:
        n_ = (n, rand.randint(0, N_MAX))
        pos_dict[n_] = n_
        graph_map[n] = n_
        abstract_G.add_node(n_)

    # add edges to abstract_G

    edge_list = G.edges()
    edge_list_ = map(lambda e: (graph_map[e[0]], graph_map[e[1]]), edge_list)
    abstract_G.add_edges_from(edge_list_)

#    nx.draw_networkx(abstract_G, pos=pos_dict, with_labels=True)
#    plt.show()

    return Graph(abstract_G, 'test_random')


# generates custom graphs to to test the correctness of the abstraction

def custom_graph(ID, num_dim):
    if num_dim != 2:
        raise NotImplementedError
    if ID == 1:
        return csg1()
    else:
        raise NotImplementedError


def csg1():
    G = nx.DiGraph()
    MAX_N = 10

    init_state = (0, 0)
    final_state = (MAX_N + 1, MAX_N + 1)
    edge_list = [((n, n), (n + 1, n + 1)) for n in range(1, MAX_N)]
    G.add_edge(init_state, edge_list[0][0])
    G.add_edges_from(edge_list)
    G.add_edge(edge_list[-1][-1], final_state)
    return Graph(G, 'test_csg1')


#    print G.nodes()
#    print G.edges()
#    plt.figure()
#    Graph(G).draw_2d()
#    plt.show()

# import networkx as nx
# import heapq
# from ModifiedDijkstra import ModifiedDijkstra

class YenKShortestPaths(object):

    """
     This is a straight forward implementation of Yen's K shortest loopless
     path algorithm. No attempt has been made to perform any optimization that
     have been suggested in the literature. Our main goal was to have a
     functioning K-shortest path  algorithm. This implementation should work
     for both undirected and directed  graphs. However it has only been tested
     so far against undirected graphs.
    """

    def __init__(
        self,
        graph,
        weight='weight',
        cap='capacity',
        ):
        """
        Constructor
        """

        self.wt = weight
        self.cap = cap
        self.g = graph
        self.pathHeap = []  # Use the heapq module functions heappush(pathHeap, item) and heappop(pathHeap, item)
        self.pathList = []  # Contains WeightedPath objects
        self.deletedEdges = set()
        self.deletedNodes = set()
        self.kPath = None

        # Make a copy of the graph tempG that we can manipulate

        if isinstance(graph, nx.Graph):

            # self.tempG = graph.copy()

            if nx.is_directed(graph):
                self.tempG = nx.DiGraph(graph)
            else:
                self.tempG = nx.Graph(graph)
        else:
            self.tempG = None

    def findFirstShortestPath(self, source, dest):
        """
        This function is called to initialize the k-shortest path algorithm.
        It also finds the shortest path in the network.
        You can use this function to restart the algorithm at anytime with
        possibly different source and destination values.
        @param source    The beginning node of the path.
        @param dest      The termination node of the path.
        @return          The shortest path or null if the path doesn't exist.
        """

        # Used to initialize or reinitialize the algorithm
        # Computes the shortest path via Dijsktra

        self.kPath = None
        self.pathHeap = []
        self.pathList = []
        self.source = source
        self.dest = dest

        # Compute the shortest path
        # nodeList = nx.dijkstra_path(self.g, source, dest, self.wt)

        alg = ModifiedDijkstra(self.g, self.wt)
        nodeList = alg.getPath(source, dest, as_nodes=True)
        if len(nodeList) == 0:
            return None
        deletedLinks = set()
        self.kPath = WeightedPath(nodeList, deletedLinks, self.g, wt=self.wt,
                                  cap=self.cap)
        self.kPath.dNode = source
        self.pathList.append(self.kPath)
        return self.kPath

    def getNextShortestPath(self):
        """
        Use this function to compute successive shortest path. Each one will have
        a length (cost) greater than or equal the previously generated algorithm.
        Returns null if no more paths can be found.
        You must first call findFirstShortestPath(source, dest) to initialize the
        algorithm and set the source and destination node.
        @return  the next shortest path (or the next longer path depending on
        how you want to think about things).
        """

        if self.kPath == None:
            raise UserWarning('Must call findFirstShortestPath before this method or no path exists'
                              )

        # Iterate over all the nodes in kPath from dNode to the node before the destination
        # and add candidate paths to the path heap.

        kNodes = self.kPath.nodeList
        index = kNodes.index(self.kPath.dNode)
        curNode = kNodes[index]
        while curNode != self.dest:
            self._removeEdgesNodes(curNode)
            candidate = self._computeCandidatePath(curNode)
            self._restoreGraph()
            if candidate != None:
                heapq.heappush(self.pathHeap, candidate)
            index = index + 1
            curNode = kNodes[index]

        if len(self.pathHeap) == 0:
            return None
        p = heapq.heappop(self.pathHeap)  # after iterations contains next shortest path
        self.pathList.append(p)
        self.kPath = p  # updates the kth path
        return p

    def _removeEdgesNodes(self, curNode):
        """
        Remove all nodes from source to the node before the current node in kPath.
        Delete the edge between curNode and the next node in kPath
        Delete any edges previously deleted in kPath starting at curNode
        add all deleted edges to the deleted edge list.
        """

        # Figure out all edges to be removed first then take them out of the temp graph
        # then remove all the nodes from the temp graph.
        # At the start the temp graph is equal to the initial graph.

        self.deletedEdges = set()
        self.deletedNodes = set()
        kNodes = self.kPath.nodeList
        index = 0
        tempNode = kNodes[index]
        index += 1
        while tempNode != curNode:
            edges = self.tempG.edges(tempNode)
            if len(edges) != 0:
                for edge in edges:
                    self.deletedEdges.add(edge)
                    self.tempG.remove_edge(edge[0], edge[1])

            #

            self.deletedNodes.add(tempNode)
            self.tempG.remove_node(tempNode)
            tempNode = kNodes[index]
            index += 1

        # Also need to remove those old deleted edges that start on curNode

        oldDelEdges = self.kPath.deletedEdges
        if self.g.is_directed():
            outEdges = self.g.out_edges(curNode)
        else:
            outEdges = self.g.edges(curNode)

        # outEdges = self.g.edges(curNode)

        for e in outEdges:
            if e in oldDelEdges:
                self.deletedEdges.add(e)
                self.tempG.remove_edge(e[0], e[1])

        # Now delete the edge from the curNode to the next in the path

        tempNode = kNodes[index]
        e = (curNode, tempNode)
        self.deletedEdges.add(e)
        self.tempG.remove_edge(curNode, tempNode)

    def _computeCandidatePath(self, curNode):
        """
        Compute the shortest path on the modified graph and then
        combines with the portion of kPath from the source up through
        the deviation node
        """

#        DijkstraShortestPath alg = new DijkstraShortestPath(tempG, wt);
#        List<E> ePath = alg.getPath(curNode, dest);

        # nodeList = nx.dijkstra_path(self.tempG, curNode, self.dest, self.wt)

        alg = ModifiedDijkstra(self.tempG, self.wt)
        nodeList = alg.getPath(curNode, self.dest, as_nodes=True)

        # Trying this out...

        if nodeList == None:
            return None

        # Get first part of the path from kPath

        nodePath = []
        if curNode in self.kPath.nodeList:
            index = self.kPath.nodeList.index(curNode)
            nodePath = self.kPath.nodeList[0:index]

        nodePath.extend(nodeList)
        wp = WeightedPath(nodePath, self.deletedEdges, self.g, wt=self.wt,
                          cap=self.cap)
        wp.dNode = curNode
        return wp

    def _restoreGraph(self):
        """
        Using the internal deleted node and deleted edge containers
        restores the temp graph to match the graph g.
        """

        # self.tempG = self.g.copy()

        if nx.is_directed(self.g):
            self.tempG = nx.DiGraph(self.g)
        else:
            self.tempG = nx.Graph(self.g)
        self.deletedEdges = []
        self.deletedNodes = []


class WeightedPath(object):

    """Used internally by the Yen k-shortest path algorithm.
    Also return to user as a result.
    """

    def __init__(
        self,
        pathNodeList,
        deletedEdges,
        g,
        wt='weight',
        cap='capacity',
        ):
        """
        Constructor
        """

        self.nodeList = pathNodeList
        self.deletedEdges = set(deletedEdges)
        self.g = g
        self.wt = wt
        self.dNode = None  # The deflection node
        self.cost = 0.0
        self.capacity = float('inf')

        # print "WtPath pathNodeList: {}".format(pathNodeList)

        for i in range(len(pathNodeList) - 1):
            self.cost = self.cost + g[pathNodeList[i]][pathNodeList[i + 1]][wt]

################################# ADI: Do we need this? ##############################
####            if not cap == None:
####                self.capacity = min(self.capacity, g[pathNodeList[i]][pathNodeList[i+1]][cap])
####            else:
####                self.capacity = None
######################################################################################

    def __cmp__(self, other):
        if other == None:
            return -1
        return cmp(self.cost, other.cost)

    def __str__(self):
        return 'nodeList: {}, cost: {}, capacity: {}'.format(self.nodeList,
                self.cost, self.capacity)


class ModifiedDijkstra(object):

    """
    The Modified Dijkstra algorithm from "Survivable Networks" by Ramesh Bhandari.
    This algorithm works with graphs that can have directed or undirected links.
    In addition, this algorithm can correctly function in some cases of negative
    arc lengths that arise in the disjoint path computations.

    Works with graphs, *g*, in NetworkX format. Specifically Graph and
    DiGraph classes.
    """

    def __init__(self, g, wt='weight'):
        """
        Constructor. Parameter *g* is a NetworkX Graph or DiGraph instance.
        The *wt* keyword argument sets the link attribute to be used in computing
        the path length.
        """

        self.dist = {}  # A map from nodes to their labels (float)
        self.predecessor = {}  # A map from a node to a node
        self.g = g
        self.wt = wt
        edges = g.edges()

        # Set the value for infinite distance in the graph

        self.inf = 0.0
        for e in edges:
            self.inf += abs(g[e[0]][e[1]][wt])
        self.inf += 1.0

    def getPath(
        self,
        source,
        dest,
        as_nodes=False,
        ):
        """
        Computes the shortest path in the graph between the given *source* and *dest*
        node (strings).  Returns the path as a list of links (default) or as a list of
        nodes by setting the *as_nodes* keyword argument to *True*.
        """

        self.dist = {}  # A map from nodes to their labels (float)
        self.predecessor = {}  # A map from a node to a node

        # Initialize the distance labels to "infinity"

        vertices = self.g.nodes()
        for vertex in vertices:
            self.dist[vertex] = self.inf
            self.predecessor[vertex] = source

        # Further set up the distance from the source to itself and
        # to all one hops away.

        self.dist[source] = 0.0
        if self.g.is_directed():
            outEdges = self.g.out_edges([source])
        else:
            outEdges = self.g.edges([source])
        for edge in outEdges:
            self.dist[edge[1]] = self.g[edge[0]][edge[1]][self.wt]

        s = set(vertices)
        s.remove(source)
        currentMin = self._findMinNode(s)
        if currentMin == None:
            return None
        s.remove(currentMin)
        while currentMin != dest and len(s) != 0 and currentMin != None:
            if self.g.is_directed():
                outEdges = self.g.out_edges([currentMin])
            else:
                outEdges = self.g.edges([currentMin])
            for edge in outEdges:
                opposite = edge[1]
                if self.dist[currentMin] + self.g[edge[0]][edge[1]][self.wt] \
                    < self.dist[opposite]:
                    self.dist[opposite] = self.dist[currentMin] \
                        + self.g[edge[0]][edge[1]][self.wt]
                    self.predecessor[opposite] = currentMin
                    s.add(opposite)

            currentMin = self._findMinNode(s)

            # print "Current min node {}, s = {}".format(currentMin, s)

            if currentMin == None:
                return None
            s.remove(currentMin)

        # Compute the path as a list of edges

        currentNode = dest
        predNode = self.predecessor.get(dest)
        node_list = [dest]
        done = False
        path = []
        while not done:
            path.append((predNode, currentNode))
            currentNode = predNode
            predNode = self.predecessor[predNode]
            node_list.append(currentNode)
            done = currentNode == source
        node_list.reverse()
        if as_nodes:
            return node_list
        else:
            return path

    def _findMinNode(self, s):
        """
        Finds the vertex with the minimum distance label in the set "s".
        returns the minimum vertex
        """

        minNode = None
        minVal = self.inf
        for vertex in s:
            if self.dist[vertex] < minVal:
                minVal = self.dist[vertex]
                minNode = vertex
        return minNode


