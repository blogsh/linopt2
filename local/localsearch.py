import numpy as np
import scipy.optimize as opt
import subprocess as sp
import os, re

os.environ['PATH'] += ":/home/sebastian/.ampl"

class Problem:
	N = 10
	T = 100
	d = 20

	c = np.array([34, 25, 14, 21, 16, 3, 10, 5, 7, 10])
	U = np.array([42, 18, 90, 94, 49, 49, 34, 90, 37, 11])

problem = Problem()

def write_params(p, z):
	ilist = ' '.join('%d' % i for i in range(1, p.N+1))
	clist = ' '.join('%d' % ci for ci in p.c)
	Ulist = ' '.join('%d' % Ui for Ui in p.U)
	tlist = ' '.join('%d' % t for t in range(1, p.T+1))
	zlist = ' '.join('%d' % zi for zi in z)

	params = []
	params.append('set Components := %s;' % ilist)
	params.append('param T := %d;' % p.T)
	params.append('param d := %d;' % p.d)
	params.append('param c : %s := 1 %s;' % (ilist, clist))
	params.append('param U : %s := 1 %s;' % (ilist, Ulist))
	params.append('param z : %s := 1 %s;' % (tlist, zlist))

	with open('uh-gen.dat', 'w+') as f:
		f.write('\n'.join(params))

def solve_lp(p, z):
	write_params(p, z)
	args = ('/home/sebastian/.ampl/ampl', 'uh.run')
	devnull = open(os.devnull, 'w')
	output = str(sp.check_output(args, env=os.environ, stderr=devnull))
	feasible = output.find('optimal solution') > -1
	output = output.split('\\n')[-4:-1]
	
	J = float(re.sub('[^0-9.]', '', output[0]))
	z = np.array(output[1].split(' '), dtype=np.float)
	x = np.array(output[2].split(' '), dtype=np.float).reshape((p.N, p.T))

	return feasible, J, z, x

def generate_neighborhood(z):
	zs = []

	for i in range(len(z)):
		zc = np.copy(z)
		zc[i] = 1 - zc[i]
		zs.append(zc)

	return zs

def search_neighborhood(p, z, J):
	neighborhood = generate_neighborhood(z)
	
	bestJ = J
	best = None

	for zi in neighborhood:
		feasible, Ji, zi, xi = solve_lp(p, zi)

		if feasible and Ji < bestJ:
			best = (Ji, zi, xi)
			bestJ = Ji

	return best

def localsearch(p, z0, K, Kn = 5):
	feasible, Jc, zc, xc = solve_lp(p, z0)

	if not feasible: 
		raise "Local search needs a feasible start solution!"

	print('   Iteration 0: J = %d' % Jc)

	for k in range(1,K+1):
		best = search_neighborhood(p, zc, Jc)

		if best is not None:
			Jc = best[0]
			zc = best[1]
			xc = best[2]

		if best is not None or k % Kn == 0:
			star = '*' if best is not None else ' '
			print('%s  Iteration %d: J = %d' % (star, k, Jc))

	return Jc, xc, zc
