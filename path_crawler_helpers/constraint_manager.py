#import fileOps as fo
import err

TRUE = 'True'


#path_list = [
#    [13, 17, 25, 27],
#    [13, 17, 25, 22],
#    [13, 17, 15],
#    [13, 8, 11],
#    [13, 8, 1, 6]
#    ]


CTR = 0


# constraint tree:
# Has been tailored specially towards handling constraints
class Tree(object):
    def __init__(self):
        self.root = Node(ID=hash('root'), data=None)

    def compute_paths(self):
        node = self.root
        #ctr = 0

        def compute(node):
            if node.children:
                s = 0
                num_children = len(node.children)
                #[comment out]: can have more than two children...!
                #if num_children > 2:
                    #raise err.Fatal('More than 2 children: {}'.format(num_children))
                for c in node.children:
                    s += compute(c)
                return s
            else:
                return 1

        ctr = compute(node)
        return ctr

    #def pretty_print(self):
    #    node = self.root
    #    num_tabs = [0]
    #
    #    def traverse(node):
    #        print node.data
    #        num_tabs[0] += 1
    #        tabs = '    '*(num_tabs[0]+1)
    #        for c in node.children:
    #            print tabs + '|---',
    #            traverse(c)
    #        num_tabs[0] -= 1
    #
    #    traverse(node)

    def __str__(self):
        s = ['']
        node = self.root
        num_tabs = [0]

        def traverse(node):
            s[0] += str(node.data) + '\n'
            num_tabs[0] += 1
            tabs = '    '*(num_tabs[0]+1)
            for c in node.children:
                s[0] += tabs + '|---'
                traverse(c)
            num_tabs[0] -= 1

        traverse(node)
        return s[0]

    def flatten(self):
        node = self.root

        def traverse(node):
            path_list = []
            if node.children:
                for c in node.children:
                    path_list += traverse(c)
                for idx, path in enumerate(path_list):
                    # change path_list in place
                    path_list[idx] = [node] + path
            else:
                path_list += [[node]]
                # also correct
                #path_listi = [[node]]
            return path_list

        return traverse(node)


class Node(object):

    def __init__(self, ID, data, **kwargs):#, children_list=None):
        self.data = data
        self.children = set()
        self.ID = ID
        self.__dict__.update(kwargs)

    def add_child(self, c):
        #c.depth = self.depth + 1
        #self.children.append(c)
        self.children.add(c)

    def add_data(self, data):
        self.data = data

    def fetch_child_using_ID(self, ID):
        for c in self.children:
            if c.ID == ID:
                return c
            else:
                return None

    def __str__(self):
        return str(self.data)

    def __str__old(self):
        s = ''
        data_str = str(self.data)
        s += data_str
        for c in self.children:
            tabs = '    '*(self.depth+1)
            s += '\n' + tabs + '|---' + str(c)
        return s

    def __repr__(self):
        return str(self.data)


def create_cons_tree_sample(path_list):
    node_table = {}
    tree = Tree()
    node = tree.root
    node_table[node.ID] = node
    for path in path_list:
        for c in path:
            # hash of constraint
            # constraint itself
            ID = hash(c)
            child_node = node_table.get(ID)
            if child_node is None:
                child_node = Node(ID=ID, data=c)
                node_table[child_node.ID] = child_node
                node.add_child(child_node)
            #print node.children
            #print data
            #print node.__repr__(), '-->', child_node.__repr__()
            #node.add_child(child_node)
            node = child_node
        node = tree.root
    return tree

# TODO: add unit tests!
