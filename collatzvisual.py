import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add nodes for powers of 2 up to 2^8
powers = list(range(8, -1, -1))  # 8 down to 0
nodes = [(i, 2**i) for i in powers]

# Add nodes with positions
pos = {}
for i, (power, value) in enumerate(nodes):
    # Stagger Class A and Class B horizontally
    x_offset = 0.3 if power % 2 == 0 else -0.3
    G.add_node(value, pos=(x_offset, i))
    pos[value] = (x_offset, i)
    
# Add edges for division by 2
for i in range(len(nodes)-1):
    G.add_edge(nodes[i][1], nodes[i+1][1])

# Add L-type harbor connections
l_harbors = [(5, 16), (21, 64), (85, 256)]
for source, target in l_harbors:
    G.add_node(source, pos=(-1.5, pos[target][1]))
    G.add_edge(source, target)

# Add example trapdoor nodes (numbers that eventually reach the ladder)
# We'll connect them directly to powers of 2 or L-type harbors
trapdoors = [(27, 32), (17, 16), (31, 32)]  # (number, where it enters sequence)
for num, target in trapdoors:
    target_y = pos[target][1]
    G.add_node(num, pos=(-2.7, target_y + 0.3))
    G.add_edge(num, target)

plt.figure(figsize=(12, 14))
pos_list = nx.get_node_attributes(G, 'pos')

# Draw the main graph
nx.draw_networkx_edges(G, pos_list, edge_color='gray', arrows=True, 
                      arrowsize=20, width=1.5)

# Draw different types of nodes
class_a = [n for n in G.nodes() if n in [4, 16, 64, 256]]
class_b = [n for n in G.nodes() if n in [2, 8, 32, 128]]
l_type = [n for n in G.nodes() if n in [5, 21, 85]]
trapdoor_nodes = [n for n in G.nodes() if n in [27, 17, 31]]

# Draw nodes with different colors and sizes
nx.draw_networkx_nodes(G, pos_list, nodelist=class_a, node_color='lightblue', 
                      node_size=2000, label='Class A Powers')
nx.draw_networkx_nodes(G, pos_list, nodelist=class_b, node_color='salmon', 
                      node_size=2000, label='Class B Powers')
nx.draw_networkx_nodes(G, pos_list, nodelist=l_type, node_color='lightgreen', 
                      node_size=2000, label='L-type Harbors')
nx.draw_networkx_nodes(G, pos_list, nodelist=trapdoor_nodes, node_color='yellow',
                      node_size=2000, label='Example Trapdoors')

# Add labels
labels = {n: str(n) for n in G.nodes()}
nx.draw_networkx_labels(G, pos_list, labels, font_size=10)

plt.title('Power of Two Ladder Structure\nwith L-type Harbors and Trapdoors', 
         pad=20, size=14)

# Create a more spaced out legend
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
          borderaxespad=0.5,
          handletextpad=1,
          labelspacing=1.5)

plt.axis('equal')
plt.grid(False)
plt.axis('off')
plt.tight_layout()
plt.show()