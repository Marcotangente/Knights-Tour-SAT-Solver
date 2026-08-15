# Knight's Tour SAT Solver
An advanced algorithmic solver for the classic Knight's Tour problem using Propositional Logic and SAT solving techniques.

This project was developed for a Logic for Computer Science course and focuses on translating complex board constraints into Conjunctive Normal Form (CNF) to be evaluated by the Glucose3 SAT solver.

**Features**:
- Propositional logic encoding: Translates the chessboard rules and knight's movement patterns into strict logical constraints. 
- Optimized solving: Implements a dual-variable encoding strategy. By combining positional variables (p_{i,j}) with succession variables (s_{i,j}), the model maximizes unit propagations. This optimization solves the full 8x8 board roughly 12 times faster than a naive encoding.
- Symmetry breaking: Accurately calculates the exact number of unique solutions on smaller boards by identifying and filtering out axial and central symmetries.
- Uniqueness constraint generation: Explores the solution space as a rooted decision tree to procedurally generate the absolute minimum set of constraints (specific cell visits at specific move numbers) required to force a single, unique valid path.

The biggest challenge in solving the Knight's Tour via SAT is the explosion of clauses. The initial naive implementation strictly enforced that a cell could not be reached in two different numbers of moves, and that no two cells could be reached at the same time.  To optimize this, the final architecture introduces the proposition: cell $i$ is followed by cell $j$ in the path. Because a knight has at most 8 valid moves from any given position, all other succession variables can be instantly set to false. This floods the SAT solver with single-literal clauses, allowing it to instantly prune massive branches of the decision tree and resolve the 8x8 board in mere seconds.  
