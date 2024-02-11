# Simple Pocket Cube Solver

- `graph.ipynb`
  
  Creates and saves the solving graph, given possible moves and color assignment. Replicates the numbers for count of states and required moves on [wikipedia](https://en.wikipedia.org/wiki/Pocket_Cube).
  Code is not optimized, need half a minute with a single 2.7GHz core.


- `solve.ipynb`
  
  Loads the solving graph and solves for given states
  

## Solving

After creating the solving graph with `graph.ipnb`, one can easily get the 
shortest solving path with:

```{python}
from base import loadGraph, Cube

graph = loadGraph()

c = Cube('OYWW RBRR GGGG YYWB YOBO RBWO')

p = c.getPathInfo(graph)
print(' '.join(p))
```
```
R F' U2 F U' F2 U R F2 R2
```
