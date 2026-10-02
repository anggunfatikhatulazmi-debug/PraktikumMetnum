t = 0:0.1:4*pi;
x = cos(t);
y = sin(t);
z = 0.3*t;
plot3(x, y, z, 'b', 'linewidth', 1);
grid on
xlabel('x'); ylabel('y'); zlabel('z');
