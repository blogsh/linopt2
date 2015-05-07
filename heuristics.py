import numpy as np

N = 10
T = 100
d = 20
c = np.array([34, 25, 14, 21, 16, 3, 10, 5, 7, 10])
U = np.array([42, 18, 90, 94, 49, 49, 34, 90, 37, 11])

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

print(np.sum(np.sum(X), 0))
#print(np.where(z)[0])
print('NUmber of maintenances', len(np.where(z)[0]))
print(offsets)

J = 0

for t in range(T):
	for i in range(N):
		J += c[i] * X[i,t]
	J += d * z[t]

print(J)


#print([sum([c[i] * X[i,t] for i in range(N)]) + d * z[t] for t in range(T)])
