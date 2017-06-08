import numpy as np


class PageRank(object):
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

    def basic_pagerank(self, taxation, tol):
        """
        pagerank method for the basic model
        """
        # initialize the pagerank vector
        num_node = self.num_node
        graph = self.graph.copy()
        graph_inverse = self.graph_inverse.copy()

        pagerank = np.array([np.random.rand() for i in range(num_node)])
        pagerank = pagerank/sum(pagerank)

        old = pagerank*0.0
        new = pagerank.copy()

        counter = 0
        while np.linalg.norm(new - old) >= tol:
            counter += 1
            print("iteration: %d; epsilon = %f" % (counter, np.linalg.norm(new - old)))
            old = new.copy()
            for i in range(num_node):
                if i+1 not in graph_inverse:
                    new[i] = taxation*(1/float(num_node))
                else:
                    from_where = np.array(graph_inverse[i+1]).tolist()
                    weight_average = 0.0
                    for item in from_where:
                        weight_average += old[item-1]*(1/float(len(graph[item])))
                    if i+1 not in graph:
                        weight_average += old[i]
                    new[i] = (1-taxation)*weight_average + taxation*(1/float(num_node))
            return new


        # pagerank = np.array([np.random.rand() for i in range(self.num_node)])
        # pagerank = pagerank/sum(pagerank)
        #
        # old = pagerank*0.0
        # new = pagerank.copy()
        #
        # counter = 0
        # while np.linalg.norm(new - old) >= tol:
        #     counter += 1
        #     print("iteration: %d; epsilon = %f" % (counter, np.linalg.norm(new - old)))
        #     old = new.copy()
        #     for i in range(self.num_node):
        #         if i+1 not in self.graph_inverse:
        #             new[i] = taxation*(1/float(self.num_node))
        #         else:
        #             from_where = np.array(self.graph_inverse[i+1]).tolist()
        #             weight_average = 0.0
        #             for item in from_where:
        #                 weight_average += old[item-1]*(1/float(len(self.graph[item])))
        #             if i+1 not in self.graph:
        #                 weight_average += old[i]
        #             new[i] = (1-taxation)*weight_average + taxation*(1/float(self.num_node))
        # return new


    def tensor_pagerank(self, topic, taxation, tol):
        """
        pagerank method for the developed model
        """
        # initialize the vector for each user
        num_topic = len(topic)
        num_node = self.num_node
        graph = self.graph
        graph_inverse = self.graph_inverse

        pageranks = np.array([[np.random.rand() for i in range(num_node)] for j in range(num_topic)])
        pageranks = np.array([(i/sum(i)).tolist() for i in pageranks])

        olds = pageranks*0.0
        news = pageranks.copy()

        counter = 0
        while np.linalg.norm(news - olds) >= tol:
            counter += 1
            print("iteration: %d; epsilon = %f" % (counter, np.linalg.norm(news - olds)))
            olds = news.copy()
            for i in range(num_topic):
                vec = olds[i]
                tax = 0
                for j in range(num_node):
                    if j+1 not in graph_inverse:
                        news[i][j] = taxation*(1/float(num_node))
                    else:
                        from_where = np.array(graph_inverse[j+1]).tolist()
                        weight_average = 0.0
                        for item in from_where:
                            weight_average += vec[item-1]*topic[i][item-1]*(1/float(len(graph[item])))
                            tax += vec[item-1]*(1-topic[i][item-1])*(1/float(len(graph[item])))
                        if j+1 not in graph:
                            weight_average += vec[j]*topic[i][j]
                            tax += vec[j]*(1-topic[i][j])
                        news[i][j] = (1-taxation)*weight_average + taxation*(1/float(num_node))
                news[i] = news[i] + (1-taxation)*tax/float(num_node)
        return news

        # pageranks = np.array([[np.random.rand() for i in range(self.num_node)] for j in range(num_topic)])
        # pageranks = np.array([(i/sum(i)).tolist() for i in pageranks])
        #
        # olds = pageranks*0.0
        # news = pageranks.copy()
        #
        # counter = 0
        # while np.linalg.norm(news - olds) >= tol:
        #     counter += 1
        #     print("iteration: %d; epsilon = %f" % (counter, np.linalg.norm(news - olds)))
        #     olds = news.copy()
        #     for i in range(num_topic):
        #         vec = olds[i]
        #         tax = 0
        #         for j in range(self.num_node):
        #             if j+1 not in self.graph_inverse:
        #                 news[i][j] = taxation*(1/float(self.num_node))
        #             else:
        #                 from_where = np.array(self.graph_inverse[j+1]).tolist()
        #                 weight_average = 0.0
        #                 for item in from_where:
        #                     weight_average += vec[item-1]*topic[i][item-1]*(1/float(len(self.graph[item])))
        #                     tax += vec[item-1]*(1-topic[i][item-1])*(1/float(len(self.graph[item])))
        #                 if j+1 not in self.graph:
        #                     weight_average += vec[j]*topic[i][j]
        #                     tax += vec[j]*(1-topic[i][j])
        #                 news[i][j] = (1-taxation)*weight_average + taxation*(1/float(self.num_node))
        #         news[i] = news[i] + (1-taxation)*tax/float(self.num_node)
        # return news
