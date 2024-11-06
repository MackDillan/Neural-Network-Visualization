# Neural Network Visualization

This project visualizes the structure of a neural network, including layers, neurons, and connections, using `NetworkX` and `Plotly`. The network structure is read from a JSON file and represented as a directed graph with detailed tooltips and interactive display.

## Overview

The script processes a JSON file containing neural network structure data and visualizes each neuron and connection in the network. The neurons are grouped by layers and plotted along vertical lines to represent each layer's depth. Edge weights are shown between neurons as tooltips, making it possible to understand the flow and weights of connections within the network.

## Features

- **Directed Graph Representation**: The network is represented as a directed graph where each neuron is a node, and each connection is an edge.
- **Interactive Visualization**: Visualized with `Plotly`, each neuron and connection shows relevant information on hover.
- **Layer-Based Layout**: Layers are organized as vertical lines with connections spanning across layers.
- **Edge Weights**: Edge weights are displayed on hover for each connection.# Neural-Network-Visualization

## Model used (MNIST dataset)
```
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(20, activation='relu'),
    Dense(10, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
```



