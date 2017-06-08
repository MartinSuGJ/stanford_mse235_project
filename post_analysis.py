import networkx as nx
import numpy as np
from PageRank import PageRank
from HITS import HITS
import os

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
    coverage = 1
    node_seen = {str(start): 0}
    ng.node[str(start)][attr] = 1
    queue = [str(start)]
    pointer = 0
    coverage_list = []
    while len(queue) > 0:
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

"""
Randomly generate the topic probablity
"""
num_topic = 7
num_node = 81306
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



"""
Analysis
"""
# Use networkx to read the twitter network
G=nx.read_edgelist("twitter_graph.txt",create_using=nx.DiGraph())
## First Method: In_Degree
in_degree = G.in_degree()
out_degree = G.out_degree()
sorted_in_degree = sorted(in_degree, key=in_degree.get, reverse=True)

num_topic = 7
num_node = 81306
topic_1 = dict()
for i in range(num_topic):
    topic_1[i] = np.array([1.0 for j in range(num_node)])

## Second Method: BFS
# steps = 10
# in_degree_x_list = dict()
# for node in G.node.keys():
#     print node
#     ng, coverage_list = info_diff(G, 'test', node, topic, 0, steps)
#     in_degree_x_list[node] = coverage_list

# Load the BFS result
file_names = '/Users/guangjun/Google Drive/Courses/2017 Spr/MS&E235/Project/BFS_Result'
bfs_result = dict()
bfs_result_type = 'basic'
for f in os.listdir(file_names):
    if bfs_result_type in f:
        bfs_result.update(pickle.load(open(file_names+"/"+f, 'rb')))

weight = 0.8
bfs_result_change = dict()
for item in bfs_result:
    degrees = bfs_result[item]
    degrees_new = [num for num in degrees]
    if len(degrees) == 9:
        for i in range(1,9):
            degrees_new[i] = degrees_new[i-1] + (degrees[i] - degrees[i-1])*weight**(i)
        bfs_result_change[item] = degrees_new

# rank the BFS result by 10 steps
bfs_degree = [0 for i in range(num_node)]
for item in bfs_result_change:
    item_id = int(item) - 1
    if len(bfs_result_change[item]) == 9:
        bfs_degree[item_id] = bfs_result_change[item][2]

bfs_degree_rank = np.argsort(-np.array(bfs_degree))



# Read the cluster file and initialize the probablistic vector
cluster_file = open("twitter_probability_initialization.csv", "r")
for line in cluster_file:
    line = line.replace('\n','').split(',')
    if line[0] == 'id':
        continue
    G.node[line[0]]["cluster"] = int(line[1])
cluster_file.close()



"""
Parameters
"""
taxation = 0.2
tol = 1e-5

# path to twitter graph file
graph = "twitter_combined.txt"

## PageRank
pg = PageRank(graph)
pg_value = pg.basic_pagerank(taxation, tol)
t_pg_value = pg.tensor_pagerank(topic, taxation, tol)

## HITS
hits = HITS(graph)
hits_h_value, hits_a_value = hits.basic_hits(tol)
t_hits_h_value, t_hits_a_value = hits.tensor_hits(topic, taxation, tol)


## Find the top influential nodes based on different
pg_value_rank = np.argsort(-pg_value)
t_pg_value_rank = []
for i in range(len(t_pg_value)):
    t_pg_value_rank.append(np.argsort(-t_pg_value[i]))

hits_h_value_rank = np.argsort(-hits_h_value)
t_hits_h_value_rank = []
for i in range(num_topic):
    t_hits_h_value_rank.append(np.argsort(-t_hits_h_value[i]))

hits_a_value_rank = np.argsort(-hits_a_value)
t_hits_a_value_rank = []
for i in range(num_topic):
    t_hits_a_value_rank.append(np.argsort(-t_hits_a_value[i]))

"""
Output the top 10 ranking of each method
"""
## Output the top 10 ranking for each topic
for i in range(num_topic):
    print t_hits_a_value_rank[i]

## Ouput the in degree of top 10 ranking for each topic
for i in range(num_topic):
    nodes = t_pg_value_rank[i][:10]
    in_degres_vec = []
    for node in nodes:
        in_degres_vec.append(in_degree[str(node+1)])
    print in_degres_vec

## Ouput the topic of top 10 ranking for each topic
for i in range(num_topic):
    nodes = t_hits_a_value_rank[i][:10]
    in_degres_vec = []
    for node in nodes:
        in_degres_vec.append(G.node[str(node+1)]['cluster'])
    print in_degres_vec




## compute the coverage list as the step size increases
start_nodes_list = [1,2]
attr_name_list = ["pk1","pk2"]
coverage_list = []
time_limit = 10
ng = G.copy()
for i,start in enumerate(start_nodes_list):
    attr = attr_name_list[i]
    ng, coverage_list = info_diff(ng, attr, start, topic, 0, time_limit)
    coverage_list.appen(coverage)


"""
1. 画折线图，看不同的步数情况下，从每一个点出发会覆盖多少点
2. 画social network图，对比不同的点，直观看coverage的对比情况
"""
topic = dict()
for i in range(num_topic):
    topic[i] = np.array([1.0 for j in range(num_node)])
## Line Chart
import matplotlib.pyplot as plt
start = '1'
steps = 3
coverage_list = []
for step in range(1,steps):
    ng, coverage = info_diff(G, 'test', start, topic, 0, step)
    coverage_list.append(coverage)

figure = plt.figure()
plt.plot(range(1,steps), coverage_list)
plt.show()



nx.write_gexf(G, "example_small.gexf")



sim_times = 500
nodes = [1759,1551,8225,277,2240,64,91,437]
steps = 10

influence = dict()

for node in nodes:
    print node
    influence[node] = np.array([0.0 for i in range(steps)])
    for i in range(sim_times):
        ng, coverage_list = info_diff(G, 'test', node, topic, 1, steps)
        for j,item in enumerate(coverage_list):
            influence[node][j] += item
    influence[node] = influence[node]/float(sim_times)
