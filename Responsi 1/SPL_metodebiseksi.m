% Perbaikan Kasus 3: Persamaan Non-Linier (Metode Biseksi)
clear; clc;

% Menggunakan titik (.^3) dan nilai pi langsung agar aman di GNU Octave
f = @(r) (4/3) * 3.141592653589793 * (r.^3) - 300;

% Visualisasi grafik untuk memastikan daerah akar
r_val = linspace(0, 5, 100);
y_val = f(r_val);

figure;
plot(r_val, y_val, 'b-', 'LineWidth', 1.5);
grid on;
title('Grafik Fungsi f(r) = (4/3)*pi*r^3 - 300');
xlabel('Jari-jari (r)');
ylabel('f(r)');

% Menentukan batas awal interval [a, b]
a = 1;
b = 5;
tol = 1e-6;
max_iter = 100;

% Pengecekan apakah interval mengapit akar
if f(a) * f(b) > 0
    a = 0;
    b = 10;
end

if f(a) * f(b) > 0
    error('Interval awal [a, b] tidak mengapit akar. Periksa kembali nilai a dan b.');
end

% Algoritma Biseksi menggunakan perulangan while
iter = 0;
c = a;

while (b - a) / 2 > tol && iter < max_iter
    iter = iter + 1;
    c = (a + b) / 2;

    if f(c) == 0
        break;
    end

    if f(a) * f(c) < 0
        b = c;
    else
        a = c;
    end
end

% Menampilkan Hasil di Command Window
fprintf('=== HASIL PENYELESAIAN KASUS 3 ===\n');
fprintf('Jumlah iterasi yang dilakukan : %d\n', iter);
fprintf('Nilai jari-jari (r)          : %.6f cm\n', c);

% Menghitung volume bagian tabung di luar bola: V = (2/3) * pi * r^3
V_luar = (2/3) * 3.141592653589793 * (c^3);
fprintf('Volume tabung di luar bola   : %.6f cm^3\n', V_luar);
