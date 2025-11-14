from pysat.solvers import Glucose3
import random
def question1(M, N, i0, j0):
	solver = Glucose3() 
	
	# YOUR CODE HERE
	solution = [[-1 for _ in range(N)] for _ in range(M)] # M x N matrix

	first_cell = indices_to_cell_number(N, i0, j0)

	###### positions variables ######

	position_variables = [[get_unique_variable() for _ in range(M*N)] for _ in range(M*N)]
	# positions p_{i,j} means the cell i is in position j in the path

	# the first cell is in position 0
	solver.add_clause([position_variables[first_cell][0]])

	# the first cell is not in position other than 0
	for pos in range(1, M*N):
		solver.add_clause([-position_variables[first_cell][pos]])

	# no cell other than the first can be in position 0
	for cell in range(M*N):
		if cell != first_cell:
			solver.add_clause([-position_variables[cell][0]])

	for cell in range(M*N):
		# all cells are in the path
		solver.add_clause(position_variables[cell])
		for pos1 in range(M*N):
			for pos2 in range(pos1+1, M*N):
				# the same cell have only 1 position in the path
				solver.add_clause([
					-position_variables[cell][pos1],
					-position_variables[cell][pos2]
					])

	for cell1 in range(M*N):
		for cell2 in range(cell1+1, M*N):
			for pos in range(M*N):
				# two cells can't be in the same position in the path
				solver.add_clause([
					-position_variables[cell1][pos],
					-position_variables[cell2][pos]
					])

	for cell1 in range(M*N):
		for pos in range(M*N - 1): # no position constraint for the last cell
			clause_possible_destinations = [-position_variables[cell1][pos]]
			for cell2 in range(M*N):
				if is_move_possible(M, N, cell1, cell2):
					# if a cell is at position i, then the cell at position i+1 is one of the allowed cells (knight)
					clause_possible_destinations.append(position_variables[cell2][pos+1])
			solver.add_clause(clause_possible_destinations)

	###### successors variables ######

	# do not create variable when the move is impossible
	successors_variables = [[None for _ in range(M*N)] for _ in range(M*N)]
	for i in range(M*N):
		for j in range(M*N):
			if is_move_possible(M, N, i, j):
				successors_variables[i][j] = get_unique_variable() # type: ignore

	# successors s_{i,j} means the cell j follow the cell i in the path

	# the first cell have no predecessor
	for predecessor in range(M*N):
		var = successors_variables[predecessor][first_cell]
		if var is not None:
			solver.add_clause([-var])

	# each cell should have a predecessor XOR is the first cell
	for cell in range(M*N):
		clause = [position_variables[cell][0]]
		for predecessor in range(M*N):
			var = successors_variables[predecessor][cell]
			if var is not None:
				clause.append(var)
		solver.add_clause(clause)

		for predecessor in range(M*N):
			var = successors_variables[predecessor][cell]
			if var is not None:
				solver.add_clause([
					-position_variables[cell][0],
					-var
				])

	# each cell should have a successor XOR is the last cell
	for cell in range(M*N):
		clause = [position_variables[cell][M*N - 1]]
		for successor in range(M*N):
			var = successors_variables[cell][successor]
			if var is not None:
				clause.append(var)
		solver.add_clause(clause)

		for successor in range(M*N):
			var = successors_variables[cell][successor]
			if var is not None:
				solver.add_clause([
					-position_variables[cell][M*N - 1],
					-var
				])

	# max 1 predecessor
	for cell in range(M*N):
		for pred1 in range(M*N):
			for pred2 in range(pred1+1, M*N):
				var1 = successors_variables[pred1][cell]
				var2 = successors_variables[pred2][cell]
				if var1 is not None and var2 is not None:
					solver.add_clause([
						-var1,
						-var2
						])

	# max 1 successor
	for cell in range(M*N):
		for succ1 in range(M*N):
			for succ2 in range(succ1+1, M*N):
				var1 = successors_variables[cell][succ1]
				var2 = successors_variables[cell][succ2]
				if var1 is not None and var2 is not None:
					solver.add_clause([
						-var1,
						-var2
						])

	# the relation pred-succ can never be symetric !!! (very useful)
	for cell1 in range(M*N):
		for cell2 in range(M*N):
			var1 = successors_variables[cell1][cell2]
			var2 = successors_variables[cell2][cell1]
			if var1 is not None and var2 is not None:
				solver.add_clause([
					-var1,
					-var2
					])

	###### clauses with position and successor variables ######

	# if (c1 is in pos p and c2 is the successor of c1) then c2 is in pos p+1
	for cell1 in range(M*N):
		for cell2 in range(M*N):
			for pos in range(M*N-1):
				var = successors_variables[cell1][cell2]
				if var is not None:
					solver.add_clause([
						-position_variables[cell1][pos],
						-var,
						position_variables[cell2][pos+1]
					])

	### solution representation
	if solver.solve():
		model = solver.get_model()
		if model is not None:
			transform_model_in_solution(model, solution, position_variables, M, N)


	reset_variables_for_next_solve()
	return solution, solver, [position_variables, successors_variables]

def question3():
	nb_sol = 0

	# YOUR CODE HERE
	M = 3
	N = 4
	for x in range(M):
		for y in range(N):
			_, solver, vars = question1(M, N, x, y)
			if solver.solve():
				nb_sol += 1
				while add_clauses_for_other_model(solver, vars, M, N, True):
					if solver.solve():
						nb_sol += 1

	return nb_sol

def question4(): 
	nb_sol = 0

	# YOUR CODE HERE
	M = 3
	N = 4
	for x in range(M):
		for y in range(N):
			_, solver, vars = question1(M, N, x, y)
			if solver.solve():
				nb_sol += 1
				while add_clauses_for_other_model(solver, vars, M, N, False):
					if solver.solve():
						nb_sol += 1

	return nb_sol

def question5(M, N,i0,j0):
	constraints = []

	# YOUR CODE HERE
	_, solver, vars = question1(M, N, i0, j0)
	position_variables = vars[0]
	if solver.solve():
		models = []
		models.append(solver.get_model())
		while add_clauses_for_other_model(solver, vars, M, N, True):
			if solver.solve():
				models.append(solver.get_model())

		solutions = []
		for model in models:
			solution = [[-1 for _ in range(N)] for _ in range(M)]
			transform_model_in_solution(model, solution, position_variables, M, N)
			solutions.append(solution)

		while len(solutions) > 1:
			for position in range(M*N):
				cells_at_pos = []
				for solution in solutions:
					for i in range(M):
						for j in range(N):
							if solution[i][j] == position:
								cells_at_pos.append(indices_to_cell_number(N, i, j))
								#should leave the two loops buut yeah...

				unique_cells_at_pos = list(set(cells_at_pos))
				if len(unique_cells_at_pos) > 1: # have to choose a constraint
					chosen_cell = random.choice(unique_cells_at_pos)
					y, x = cell_number_to_indices(N, chosen_cell)
					constraint = (position, y, x)
					constraints.append(constraint)
					solutions = list(filter(
						lambda solution: solution[constraint[1]][constraint[2]] == constraint[0], solutions
					))
					break # no need to check further in the path

	return constraints
		

##### additional functions

UNIQUE_VARIABLE_COUNT = 0
def get_unique_variable():
    global UNIQUE_VARIABLE_COUNT
    UNIQUE_VARIABLE_COUNT += 1
    return UNIQUE_VARIABLE_COUNT

def reset_variables_for_next_solve():
	global UNIQUE_VARIABLE_COUNT
	UNIQUE_VARIABLE_COUNT = 0

# ASSUMING (i, j) IS IN BOUNDS
def indices_to_cell_number(width, i, j):
	return i * width + j

def cell_number_to_indices(width, nbr):
	i = nbr//width
	j = nbr%width 
	return i, j

def is_move_possible(height, width, cell1, cell2):
	moves = [
		[-2, +1],
		[-1, +2],
		[+1, +2],
		[+2, +1],
		[+2, -1],
		[+1, -2],
		[-1, -2],
		[-2, -1]
	]

	for move in moves:
		i, j = cell_number_to_indices(width, cell1)
		new_i = i + move[0]
		new_j = j + move[1]
		if 0 <= new_j and new_j < width and 0 <= new_i and new_i < height: #in the board
			dest = indices_to_cell_number(width, new_i, new_j)
			if dest == cell2:
				return True
 
	return False

def transform_model_in_solution(model, solution, position_variables, M, N):
	for k in range(M):
		for l in range(N):
			i = indices_to_cell_number(N, k, l)
			for j in range(M*N):
				if model[ position_variables[i][j] - 1 ] > 0:
					solution[k][l] = j

def add_clauses_for_other_model(solver: Glucose3, variables, M, N, accept_symetry = True):
	if not solver.solve():
		return False

	model = solver.get_model()
	if model is None:
		return False
	
	new_clause = []

	position_variables = variables[0]
	for list in position_variables:
		for var in list:
			if model[var - 1] > 0:
				new_clause.append(-var)

	solver.add_clause(new_clause)


	if not accept_symetry:
		solution = [[-1 for _ in range(N)] for _ in range(M)]
		transform_model_in_solution(model, solution, position_variables, M, N)
		vert_axial_sym_clause = []
		horiz_axial_sym_clause = []
		central_sym_clause = []
		for i in range(M):
			for j in range(N):
				position = solution[i][j]
				vert_axial_sym_clause.append(
					-position_variables[indices_to_cell_number(N, i, N-j-1)][position]
				)
				horiz_axial_sym_clause.append(
					-position_variables[indices_to_cell_number(N, M-i-1, j)][position]
				)
				central_sym_clause.append(
					-position_variables[indices_to_cell_number(N, M-i-1, N-j-1)][position]
				)

		solver.add_clause(vert_axial_sym_clause)
		solver.add_clause(horiz_axial_sym_clause)
		solver.add_clause(central_sym_clause)

	return True
