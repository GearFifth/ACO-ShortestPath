# Ant Colony Optimization Algorithm for the Shortest Path Problem

## Project Overview
This project demonstrates the implementation of the Ant Colony Optimization (ACO) algorithm to find the shortest path between two points within a graph.

## Problem Description
The main goal of this project is to find the shortest path between two points in a graph using the Ant Colony Optimization algorithm

## Introduction
**Ant Colony Optimization** (ACO) is an algorithm inspired by the behavior of ants in nature. Ants leave pheromone trails while searching for food, which other ants follow. In this simulation:
 - Ants aim to find the shortest path to a given target point
 - Ants leave pheromones on paths, which evaporate over time
 - Initially, all paths have equal pheromone levels, so the selection is random
 - Shorter paths get stronger pheromone trails, making them more attractive to future ants

By releasing a large number of ants over several iterations, the algorithm finds the optimal path to the target.

## Implementation
The graph is represented by nodes and edges:

 - Each node represents a point.
 - Each edge represents a path with a tuple (Euclidean distance, pheromone level).

### Steps:
 1. The graph is populated by loading points and their neighbors from a file.
 2. The algorithm initializes the pheromone level of all paths to 1.
 3. The user provides necessary parameters to start the algorithm.
 4. Ants are released and follow paths based on pheromone levels, which are updated over time.
 5. If an ant finds the target, it updates the pheromone trail on the path it took. Otherwise, no pheromone is left.

### Graph Initialization
Each node in the graph is a point, and edges represent paths between them. The initial pheromone level on all paths is set to 1.

### Pheromone Update Algorithm
After an ant completes its path, the pheromone levels are updated as follows:

![image](https://github.com/user-attachments/assets/a90c24cc-8a32-4284-bf02-149986c1c2d7)

Where:
 - `k`: Current ant number
 - `τ_ij`: Pheromone level between nodes i and j
 - `ρ`: Pheromone evaporation factor
 - `m`: Total number of ants
 - `Δτ_ij = 1 / L`: Amount of pheromone added, where L is the path length


### Next Point Selection Algorithm
Ants avoid revisiting previously visited points. The probability of selecting the next point is based on both pheromone levels and Euclidean distance:

![image](https://github.com/user-attachments/assets/de278d71-3d2a-44e7-a7a6-62155173e582)

Where:

 - `α`: Influence of pheromone levels
 - `β`: Influence of distance
 - `L_ij`: Distance between nodes i and j
Initially, α and β are both set to 1.

The algorithm calculates probabilities for all available paths and selects the next point based on cumulative probability.


## Conclusion
The performance of the ACO algorithm depends on the parameter choices:

 - A smaller number of ants and iterations results in faster execution, but the solution may not be optimal.
 - A larger number of ants and iterations yields more optimal solutions but at the cost of slower execution.

Depending on the structure of the graph and the selected points, it is possible that no ant will find the target in some cases.


## Contributors
`Ilija Bešlin (SV71/2021)`
`Branko Marić (SV70/2021)`
