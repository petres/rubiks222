# Simple Pocket Cube Solver


## Create Graph (`graph.ipynb`)
  
Creates and saves the solving graph, given possible moves and color assignment. Replicates the numbers for count of states and required moves on [wikipedia](https://en.wikipedia.org/wiki/Pocket_Cube).
Code is not optimized, need half a minute with a single 2.7GHz core. With default settings only the movements F*, R* and U* are allowed, so we have a fixed cubie (BDR).


## Solving (`solve.ipynb`)

After creating the solving graph with `graph.ipnb`, one can easily get the shortest solving path in no time with:

```python
from base import loadGraph, Cube

graph = loadGraph()

#   sides   |  side
#    0      |  1 2 
#  4 2 1 5  |  3 4 
#    3      |      
c = Cube('OYWW RBRR GGGG YYWB YOBO RBWO')

p = c.getPathInfo(graph)
print(' '.join(p))
```
```
R F' U2 F U' F2 U R F2 R2
```

For other examples see `solve.ipynb`. There is no need to put the fixed cube in the correct position, that's done via dynamic color assignment.
