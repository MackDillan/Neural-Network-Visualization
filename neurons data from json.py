import json
import networkx as nx
import plotly.graph_objects as go

# Load neural network data from JSON file
with open("neural_network_structure.json", "r") as json_file:
    nn_structure = json.load(json_file)

# Initialize directed graph
G = nx.DiGraph()

# Add neurons as nodes
for neuron in nn_structure["neurons"]:
    neuron_id = neuron["neuron_id"]
    layer_index = neuron["layer_index"]
    activation_function = neuron.get("activation_function", None)
    G.add_node(neuron_id, layer=layer_index, activation_function=activation_function)

# Add connections as edges
for connection in nn_structure["connections"]:
    from_neuron = connection["from_neuron"]
    to_neuron = connection["to_neuron"]
    weight = connection["weight"]
    bias = connection.get("bias", None)
    if from_neuron in G.nodes and to_neuron in G.nodes:
        G.add_edge(from_neuron, to_neuron, weight=weight, bias=bias)

# Determine custom positions for each node
layers = nn_structure["layers"]
pos = {}
flatten_neuron_id = None
max_layer_size = max(len(layer["neurons"]) for layer in layers)

for layer in layers:
    layer_index = layer["layer_index"]
    neurons = layer["neurons"]
    if layer["layer_type"] == "Flatten" and neurons:
        flatten_neuron_id = neurons[0]
        neurons = [flatten_neuron_id]  # Single node for Flatten layer
    num_neurons = len(neurons)
    for neuron_index, neuron_id in enumerate(neurons):
        x = neuron_index - (num_neurons - 1) / 2
        y = -layer_index * (max_layer_size / 2)
        pos[neuron_id] = (x, y)

# Edge coordinates
edge_x = []
edge_y = []
edge_text = []

for edge in G.edges(data=True):
    if edge[0] in pos and edge[1] in pos:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(f"Weight: {edge[2]['weight']:.2f}")

# Adding connections from Flatten to the next layer
if flatten_neuron_id:
    next_layer_neurons = layers[1]["neurons"] if len(layers) > 1 else []
    for to_neuron_id in next_layer_neurons:
        if flatten_neuron_id in G.nodes and to_neuron_id in G.nodes:
            G.add_edge(flatten_neuron_id, to_neuron_id, weight=1.0)
            if flatten_neuron_id in pos and to_neuron_id in pos:
                x0, y0 = pos[flatten_neuron_id]
                x1, y1 = pos[to_neuron_id]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])
                edge_text.append("Weight: 1.00")

# Node coordinates
node_x = [pos[node][0] for node in G.nodes if node in pos]
node_y = [pos[node][1] for node in G.nodes if node in pos]
node_text = [
    f"Neuron: {node}<br>Layer: {data['layer']}<br>Activation: {data['activation_function']}"
    for node, data in G.nodes(data=True) if node in pos
]

# Plot edges
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1.5, color='#888'),
    hoverinfo='text',
    mode='lines',
    text=edge_text,
    opacity=0.7
)

# Plot nodes
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=node_text,
    textposition="top center",
    hoverinfo='text',
    marker=dict(color='white', line=dict(color='black', width=2), size=20),
    textfont=dict(color='black')
)

# Create Plotly figure
fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title='Neural Network Visualization',
        titlefont_size=16,
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)

# Display the figure
fig.show()
