import numpy as np
import heuristics
import localsearch

class ProblemStor:
	N = 10
	T = 100
	d = 20

	c = np.array([34, 25, 14, 21, 16, 3, 10, 5, 7, 10])
	U = np.array([42, 18, 90, 94, 49, 49, 34, 90, 37, 11])

class ProblemData:
	N = 4
	T = 100
	d = 10

	c = np.array([5, 6, 7, 9])
	U = np.array([3, 4, 5, 7])

problem = ProblemStor()
#problem = ProblemData()

J, x, z = heuristics.heuristic(problem)
print('Heuristics: J = %d\n\nLocal search:' % J)
J, x, z = localsearch.localsearch(problem, z, 1000)
