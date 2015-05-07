import numpy as np

def heuristic(p):
	N, T, d, c, U = p.N, p.T, p.d, p.c, p.U

	z = np.zeros((T))
	z[::U[0]] = 1

	def Zi(z, offset, Ui):
		cZ = np.copy(z)
		cZ[offset::Ui] = 1
		return cZ

	offsets = [0]

	for i in range(1, N):
		offsets.append(np.argmin([
			np.sum(Zi(z, offset, U[i])) for offset in range(U[i])
		]))
		z[offsets[-1]::U[i]] = 1

	X = []

	for i in range(N):
		x = np.zeros((T))
		x[offsets[i]::U[i]] = 1
		X.append(x)

	X = np.vstack(X)

	J = 0
	for t in range(T):
		for i in range(N):
			J += c[i] * X[i,t]
		J += d * z[t]

	return J, X, z
