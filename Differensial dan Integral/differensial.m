% Differensial
pkg load symbolic
syms x
f = input('Masukkan bentuk persamaan f(x) = ');
f_asli = sym(f)
f_turunan = diff(f_asli, 'x')

