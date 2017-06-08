# Load the BFS result
topic_number = 1
file_names = '/Users/guangjun/Google Drive/Courses/2017 Spr/MS&E235/Project/BFS_Result'
bfs_result = dict()
# bfs_result_type = 'topic'+str(topic_number)
bfs_result_type = "basic"
for f in os.listdir(file_names):
    if bfs_result_type in f:
        bfs_result.update(pickle.load(open(file_names+"/"+f, 'rb')))


weight = 0.8
top_index = 10
bfs_result_change = dict()
step_num = 0
for item in bfs_result:
    degrees = bfs_result[item]
    degrees_new = [num for num in degrees]
    if len(degrees) == 9:
        for i in range(1,9):
            # degrees_new[i] = degrees_new[i-1] + (degrees[i] - degrees[i-1])*weight**(i)
            degrees_new[i] = degrees_new[i-1] + (degrees[i] - degrees[i-1])*weight
        bfs_result_change[item] = degrees_new

# rank the BFS result by 10 steps
bfs_degree = [0 for i in range(num_node)]
for item in bfs_result_change:
    item_id = int(item) - 1
    if len(bfs_result_change[item]) == 9:
        bfs_degree[item_id] = bfs_result_change[item][step_num]

bfs_degree_rank = np.argsort(-np.array(bfs_degree))


# In degree ranking
in_degree_rank = [int(item)-1 for item in sorted_in_degree[:top_index]]
# BFS ranking
bfs_degree_rank[:top_index]
# PageRank ranking
# pg_value_rank[:top_index]
t_pg_value_rank[topic_number][:top_index]
# HITS ranking
# hits_a_value_rank[:top_index]
t_hits_a_value_rank[topic_number][:top_index]

bfs_degree

x1 = [bfs_degree[item] for item in in_degree_rank]
x2 = [bfs_degree[item] for item in bfs_degree_rank[:top_index]]
x3 = [bfs_degree[item] for item in pg_value_rank[:top_index]]
x4 = [bfs_degree[item] for item in hits_a_value_rank[:top_index]]

import matplotlib.pyplot as plt
plt.plot(range(top_index), x1, 'r', x2, 'b', x3, 'y', x4, 'g')
plt.show()





# node_list = [1759, 64, 1551, 91, 79, 437, 277, 2]
node_list = [1759, 64, 1551, 91, 437, 79]
color_list = ['r','g','b','y','m','k']
for i,node in enumerate(node_list):
    node  = str(node)
    plt.plot(range(9), bfs_result_change[node], color_list[i])
plt.show()
