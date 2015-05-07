%% Define data

N = 10;
T = 125;
d = 20;

c = [35, 25, 14, 21, 16, 3, 10, 5, 7, 10];
U = [42, 18, 90, 94, 49, 49, 34, 90, 37, 11];

%% Heuristic

offsets = zeros(1, N);
z = zeros(1, T);
z(1:U(1):end) = 1;

for i = 1:N
    cZ = z;
    
    intersections = zeros(1, U(i));
    for offset = 1:U(i)
        cZ = z;
        cZ(offset:U(i):end) = 1;
        intersections(offset) = sum(cZ);
    end
    
    [~, offset] = min(intersections);
    offsets(i) = offset;
    z(offset:U(i):end) = 1;
end

%% Construct solution

x = zeros(N, T);
for i = 1:N
    x(i,offsets(i):U(i):end) = 1;
end

J = 0;
for t = 1:T
    for i = 1:N
        J = J + c(i) * x(i,t);
    end
    J = J + d * z(t);
end

%% Display solution
x
z
J
