## HITS
import numpy as np

class HITS(object):
    def __init__(self, graph):
        self.graph = dict()
        self.graph_inverse = dict()
        node = dict()
        counter = 0
        twitter_file = open(graph, 'r')
        for line in twitter_file:
            line = line.replace("\n","").split(" ")
            head = int(line[0])
            tail = int(line[1])
            if head not in node:
                counter += 1
                node[head] = counter
            if tail not in node:
                counter += 1
                node[tail] = counter

            if node[head] not in self.graph:
                self.graph[node[head]] = [node[tail]]
            else:
                self.graph[node[head]].append(node[tail])

            if node[tail] not in self.graph_inverse:
                self.graph_inverse[node[tail]] = [node[head]]
            else:
                self.graph_inverse[node[tail]].append(node[head])
        twitter_file.close()
        self.num_node = len(node)

    def basic_hits(self, tol):
        """
        Basic Hubs and Authorities Model
        """
        # initialize the hub and authority vector
        # Basic Model
        h = np.array([np.random.rand() for i in range(self.num_node)])
        a = np.array([np.random.rand() for i in range(self.num_node)])

        h_new = h.copy()
        h_old = np.array([0.0]*self.num_node)
        a_new = a.copy()
        a_old = np.array([0.0]*self.num_node)


        while np.linalg.norm(h_new-h_old) >= tol or np.linalg.norm(a_new-a_old) >= tol:
            h_old = h_new.copy()
            for i in range(self.num_node):
                if i+1 not in self.graph:
                    to_where = []
                else:
                    tos = self.graph[i+1]
                    to_where = [item-1 for item in tos]
                h_new[i] = sum(a[to_where])
            h_new = h_new/float(max(h_new))

            a_old = a_new.copy()
            for i in range(self.num_node):
                if i+1 not in self.graph_inverse:
                    from_where = []
                else:
                    froms = self.graph_inverse[i+1]
                    from_where = [item-1 for item in froms]
                a_new[i] = sum(h[from_where])
            a_new = a_new/float(max(a_new))

        return h_new, a_new

    def tensor_hits(self, topic, taxation, tol):
        """
        Developed Hubs and Authorities Model
        """
        num_topic = len(topic)

        hubs = np.array([[np.random.rand() for i in range(self.num_node)] for j in range(num_topic)])
        auts = np.array([[np.random.rand() for i in range(self.num_node)] for j in range(num_topic)])

        hubs_old = hubs*0.0
        hubs_new = hubs.copy()

        auts_old = auts*0.0
        auts_new = auts.copy()


        while np.linalg.norm(hubs_new-hubs_old) >= tol or np.linalg.norm(auts_new-auts_old) >= tol:
            # Update the hubbiness
            hubs_old = hubs_new.copy()
            for i in range(num_topic):
                vec = auts_new[i]
                tax = 0.0
                for j in range(self.num_node):
                    if j+1 not in self.graph:
                        to_where = []
                    else:
                        tos = self.graph[j+1]
                        to_where = [item-1 for item in tos]
                    hubs_new[i][j] = np.dot(vec[to_where], topic[i][to_where])
                    tax += np.dot(vec[to_where], 1.0 - topic[i][to_where])
                hubs_new[i] = hubs_new[i] + tax/float(self.num_node)
                hubs_new[i] = hubs_new[i]/max(hubs_new[i])

            # Update the authorities
            auts_old = auts_new.copy()
            for i in range(num_topic):
                vec = hubs_new[i]
                tax = 0.0
                for j in range(self.num_node):
                    if j+1 not in self.graph_inverse:
                        from_where = []
                    else:
                        froms = self.graph_inverse[j+1]
                        from_where = [item-1 for item in froms]
                    auts_new[i][j] = np.dot(vec[from_where],topic[i][from_where])
                    tax += np.dot(vec[from_where],1.0 - topic[i][from_where])
                auts_new[i] = auts_new[i] + tax/float(self.num_node)
                auts_new[i] = auts_new[i]/max(auts_new[i])

        return hubs_new, auts_new
