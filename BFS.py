# I am new new
import networkx as nx
import numpy as np
from PageRank import PageRank
from HITS import HITS
import pickle
import argparse

"""
Function
"""
## Use BFS to simulate the information diffusion
# def info_diff(ng, attr, start, topic, topic_index, time_limit):
#     for node in ng.node:
#         ng.node[node][attr] = 0
#     coverage = 1
#     node_seen = {str(start): 0}
#     ng.node[str(start)][attr] = 1
#     queue = [str(start)]
#     while len(queue) > 0:
#         current = queue.pop(0)
#         if node_seen[current] >= time_limit:
#             break
#         for node in ng.predecessors(current):
#             if np.random.rand() <= topic[topic_index][int(node)-1]:
#                 if node not in node_seen:
#                     ng.node[node][attr] = 1
#                     queue.append(node)
#                     coverage += 1
#                 node_seen[node] = node_seen[current] + 1
#
#     return ng, coverage


def info_diff(ng, attr, start, topic, topic_index, time_limit):
    for t in range(1,time_limit):
        for node in ng.node:
            ng.node[node][attr + str(t)] = 0
        ng.node[str(start)][attr + str(t)] = 1
    coverage = 1
    node_seen = {str(start): 0}
    queue = [str(start)]
    pointer = 0
    coverage_list = [1]
    while len(queue) > 0:
        # pop up the first element of the queue
        current = queue.pop(0)
        if node_seen[current] >= time_limit:
            break
        if node_seen[current] > pointer:
            pointer += 1
            coverage_list.append(coverage)
        for node in ng.predecessors(current):
            if np.random.rand() <= topic[topic_index][int(node)-1]:
                if node not in node_seen:
                    for t in range(node_seen[current]+1, time_limit):
                        ng.node[node][attr + str(t)] = 1
                    queue.append(node)
                    coverage += 1
                    node_seen[node] = node_seen[current] + 1

    return ng, coverage_list

if __name__ == "__main__":
    ## Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("type_method", help="1: Basic BFS; 2: Advanced BFS", type=int)
    parser.add_argument("start_from", help="start from where", type=int)
    parser.add_argument("end_to", help="end to where", type=int)
    parser.add_argument("topic_id", help="topic id", type=int)

    args = parser.parse_args()
    type_method = args.type_method
    start_from = args.start_from
    end_to = args.end_to
    topic_id = args.topic_id

    # Use networkx to read the twitter network
    G=nx.read_edgelist("twitter_graph.txt",create_using=nx.DiGraph())
    ## First Method: In_Degree
    in_degree = G.in_degree()
    out_degree = G.out_degree()
    sorted_in_degree = sorted(in_degree, key=in_degree.get, reverse=True)

    num_topic = 7
    num_node = 81306
    steps = 6

    if type_method == 1:
        # Basic BFS
        topic = dict()
        for i in range(num_topic):
            topic[i] = np.array([1.0 for j in range(num_node)])

        # in_degree_x_list = dict()
        # for node in G.node.keys()[start_from:end_to]:
        #     print node
        #     in_degree_x_list[node] = []
        #     for step in range(1,steps):
        #         ng, coverage = info_diff(G, 'test', node, topic, 0, step)
        #         in_degree_x_list[node].append(coverage)
        in_degree_x_list = dict()
        for node in G.node.keys()[start_from:end_to]:
            print node
            ng, coverage_list = info_diff(G, 'test', node, topic, 0, steps)
            in_degree_x_list[node] = coverage_list

        pickle.dump(in_degree_x_list, open("/home/guangjun/235/result/basic_bfs_" + str(start_from) + "_" + str(end_to) + ".p", "wb"))
        # pickle.dump(in_degree_x_list, open("/Users/guangjun/Google Drive/Courses/2017 Spr/MS&E235/Project/basic_bfs_" + str(start_from) + "_" + str(end_to) + ".p", "wb"))
    else:
        # Advanced BFS
        topic = dict()
        for i in range(num_topic):
            topic[i] = np.array([np.random.rand() for j in range(num_node)])

        cluster_file = open("twitter_probability_initialization.csv", "r")
        for line in cluster_file:
            line = line.replace('\n','').split(',')
            if line[0] == 'id':
                continue
            topic[0][int(line[0])-1] = float(line[2])
            topic[1][int(line[0])-1] = float(line[3])
            topic[2][int(line[0])-1] = float(line[4])
            topic[3][int(line[0])-1] = float(line[5])
            topic[4][int(line[0])-1] = float(line[6])
            topic[5][int(line[0])-1] = float(line[7])
            topic[6][int(line[0])-1] = float(line[8])
        cluster_file.close()

        # in_degree_x_list = dict()
        # for node in G.node.keys()[start_from:end_to]:
        #     print node
        #     in_degree_x_list[node] = []
        #     for step in range(1,steps):
        #         ng, coverage = info_diff(G, 'test', node, topic, topic_id, step)
        #         in_degree_x_list[node].append(coverage)

        in_degree_x_list = dict()
        for node in G.node.keys()[start_from:end_to]:
            print node
            ng, coverage_list = info_diff(G, 'test', node, topic, topic_id, steps)
            in_degree_x_list[node] = coverage_list

        pickle.dump(in_degree_x_list, open("/home/guangjun/235/result/advanced_bfs_topic" + str(topic_id) + "_" + str(start_from) + "_" + str(end_to) + ".p", "wb"))
        # pickle.dump(in_degree_x_list, open("/Users/guangjun/Google Drive/Courses/2017 Spr/MS&E235/Project/advanced_bfs_topic" + str(topic_id) + "_" + str(start_from) + "_" + str(end_to) + ".p", "wb"))
