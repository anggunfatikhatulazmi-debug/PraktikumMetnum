x = -5:0.5:5;
y = x;
[X, Y] = meshgrid(x, y);
Z = cos(X).*sin(Y);
mesh(X, Y, Z);
