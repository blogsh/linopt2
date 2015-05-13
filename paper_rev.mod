param T;
param d;
param B;

set Components;
set I = {s in 0..T, t in 1..(T+1): t > s};

param c{Components};
param U{Components};

var x{Components, I} >= 0 binary;
var z{1..T} >= 0 binary;

minimize Cost: sum{t in 1..T} d * z[t] 
	+ sum{i in Components, (s,t) in I : s > 0} c[i] * x[i,s,t];

subject to MaintenanceOccasions {i in Components, t in 1..T}:
	sum{s in 0..(t-1)} x[i,s,t] <= z[t];

subject to MainenanceIntervals {i in Components, t in 1..T}:
	sum{s in 0..(t-1)} x[i,s,t] = sum{r in (t+1)..(T+1)} x [i,t,r];

subject to MaintenanceStart {i in Components}:
	sum{t in 1..(T+1)} x[i,0,t] = 1;

subject to ReplaceWithinLife {i in Components, (s,t) in I : t-s > U[i]}:
	x[i,s,t] = 0;
