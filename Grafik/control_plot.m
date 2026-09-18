x = -4:0.2:4;
y = -4:0.2:4;
[X,Y] = meshgrid(x,y);
Z = 2.2.^(-1.2*sqrt(X.^2 + Y.^2)).*cos(0.6*Y).*sin(X);
contour3(X,Y,Z,18)
xlabel('x');
ylabel('y');
zlabel('z');
