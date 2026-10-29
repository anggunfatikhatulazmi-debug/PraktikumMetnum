% Kasus 1: Analisis Galat dan Deret Taylor
clear; clc; close all;

% Parameter yang diketahui
lambda = 12;
v = 36;
x = 10;
h0 = 5;
t = linspace(0, 5, 500); % Rentang t dari 0 sampai 5

% 1. Perhitungan Eksak
h_eksak = h0 * (cos((t * v) / lambda) + exp(x));

% 2. Pendekatan Deret Taylor untuk n = 23, 24, 25
% Fungsi Pendekatan Cos(x) menggunakan suku hingga orde tertentu
% Fungsi Pendekatan Exp(x)
% (Catatan: implementasi penjumlahan suku deret sesuai iterasi n)

n_list = [23, 24, 25];
h_app = zeros(length(n_list), length(t));
error_mutlak = zeros(length(n_list), length(t));

for idx = 1:length(n_list)
    n = n_list(idx);

    % Pendekatan cos(x) manual menggunakan deret hingga iterasi n
    cos_approx = 0;
    for k = 0:n
        cos_approx = cos_approx + ((-1)^k * x^(2*k)) / factorial(2*k);
    end

    % Pendekatan exp(x) manual menggunakan deret hingga iterasi n
    exp_approx = 0;
    for k = 0:n
        exp_approx = exp_approx + (x^k) / factorial(k);
    end

    % Menghitung formula gelombang pendekatan
    h_app(idx, :) = h0 * (cos_approx + exp_approx);

    % Menghitung galat mutlak terhadap nilai eksak
    error_mutlak(idx, :) = abs(h_eksak - h_app(idx, :));
end

% Visualisasi Grafik
figure;
plot(t, h_eksak, 'k-', 'LineWidth', 2); hold on;
colors = ['r', 'g', 'b'];
for idx = 1:length(n_list)
    plot(t, h_app(idx, :), 'Color', colors(idx), 'LineWidth', 1.5);
end
grid on;
title('Perbandingan Grafik Eksak dan Metode Pendekatan Taylor');
xlabel('Waktu (t)');
ylabel('Tinggi Gelombang (h)');
legend(['Eksak', arrayfun(@(n) sprintf('n = %d', n), n_list, 'UniformOutput', false)], 'Location', 'best');

% Rerata Galat Mutlak
rerata_galat = mean(error_mutlak, 2);
for idx = 1:length(n_list)
    fprintf('Rerata galat mutlak untuk n = %d adalah: %.6f\n', n_list(idx), rerata_galat(idx));
end
