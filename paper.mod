param T;
param d;
param B;

set Components;
set I = {s in 0..T, t in 1..(T+1): t > s};

param c{Components};
param U{Components};

var x{Components, I} >= 0;# binary;
var z{0..T} >= 0;# binary;

minimize Cost: sum{t in 0..T} d * z[t] 
	+ sum{i in Components, s in 1..T, t in s+1..T+1} c[i] * x[i,s,t]
	+ sum{i in Components, (s,t) in I} (if t - s > U[i] then B else 0) * x[i,s,t];

subject to MaintenanceOccasions {i in Components, t in 1..T}:
	sum{s in 0..(t-1)} x[i,s,t] <= z[t];

subject to MainenanceIntervals {i in Components, t in 1..T}:
	sum{s in 0..(t-1)} x[i,s,t] = sum{r in (t+1)..(T+1)} x [i,t,r];

subject to MaintenanceStart {i in Components}:
	sum{t in 1..(T+1)} x[i,0,t] = 1;

set XIND = {s in 0..T, t in 0..T : (s,t) in I and t <= 2*s};
subject to ComponentPeriodicity {i in Components, (s,t) in XIND}:
	x[i,s,t] = x[i,2*s-t,s];

set ZIND = {s in 0..T, t in 0..T : (s,t) in I and t <= T and t < 2*s and s > 0};
subject to MaintanancePeriodicity {(s,t) in ZIND}:
	z[s] + z[t] <= 1 + z[2*s - t];

subject to MaintenancePeriodicity2 {s in 1..T, k in 1..floor(T/s)}:
	z[s] <= z[k * s];
