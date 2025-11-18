import solution_template as st

# Necessary for visualization only
import matplotlib.pylab as pl
import numpy as np

# If you want to measure time
import time

def plot_solution(solution):
	solution_array = np.array(solution)
	M, N = solution_array.shape
	fig = pl.figure(figsize = (N * 5.0 / M, 5))
	ax = pl.gca()
	chessboard = ax.table(cellText = solution_array, cellColours = np.array([['white' if (i + j) % 2 == 0 else 'orange' for j in range(N)] for i in range(M)]),loc=(0,0), cellLoc='center', fontsize = 15)
	ax.set_xticks([])
	ax.set_yticks([])
	for i in range(M):
		for j in range(N):
			cell = chessboard[i, j]
			cell.set_height(1.0 / M)
			cell.set_width(1.0 / N)
	# pl.savefig("example-sol.pdf")
	pl.show()
	return


if __name__ == '__main__':

	# Question 1
	plot_solution(st.question1(5, 5, 0, 0)[0]) # there should be a solution
	plot_solution(st.question1(3, 7, 0, 0)[0]) # there should be a solution
	plot_solution(st.question1(7, 5, 3, 1)[0]) # there should be a solution
	plot_solution(st.question1(4, 4, 0, 0)[0]) # there should not be a solution

	# Question 2
	plot_solution(st.question1(8, 8, 0, 0)[0])

	# Question 3
	print("Number of solutions for a 3x4 chessboard: " + str(st.question3()))

	# Question 4
	print("Number of solutions for a 3x4 chessboard, up to symmetry: " + str(st.question4()))

	# Question 5
	print(st.question5(4, 4, 0, 0)) # should be the empty list
	print(st.question5(3, 4, 1, 3))
	print(st.question5(3, 4, 1, 3)) # should not systematically give the same result as the previous call