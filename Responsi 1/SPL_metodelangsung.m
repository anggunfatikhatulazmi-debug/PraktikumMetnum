% Kasus 2: SPL Metode Langsung (Eliminasi Gauss / Gauss-Jordan)
clear; clc;

% Matriks Koefisien A (setelah penyetaraan satuan ke kilogram / kg)
% Variabel kolom: [Beras; Telur; Tepung; Ayam]
A = [
    2.5,  1.5,  5.0,  0.5;   % Adel
    4.0,  0.75, 1.0,  2.0;   % Briza
    2.0,  1.5,  0.5,  6.0;   % Caca
    1.0,  4.25, 2.0,  0.9    % Dinda
];

% Vektor Konstanta B (dalam Rupiah)
B = [161000; 149000; 251500; 173000];

% Analisis Determinan untuk memastikan solusi unik
det_A = det(A);
fprintf('Determinan Matriks A: %.4f\n', det_A);

if abs(det_A) < 1e-9
    fprintf('Matriks singular atau hampir singular, sistem tidak memiliki solusi unik.\n');
else
    % Penyelesaian SPL menggunakan operasi matriks / metode langsung (Gauss-Jordan)
    [m, n] = size(A);
    Aug = [A, B]; % Augmented Matrix

    for i = 1:m
        % Pivoting partial
        [~, max_row] = max(abs(Aug(i:m, i)));
        max_row = max_row + i - 1;
        if max_row ~= i
            Aug([i, max_row], :) = Aug([max_row, i], :);
        end

        % Membuat pivot menjadi 1
        Aug(i, :) = Aug(i, :) / Aug(i, i);

        % Eliminasi baris lain
        for j = 1:m
            if j ~= i
                factor = Aug(j, i);
                Aug(j, :) = Aug(j, :) - factor * Aug(i, :);
            end
        end
    end

    harga_per_kg = Aug(:, end);

    fprintf('\nHarga per kilogram setiap bahan:\n');
    fprintf('1. Beras  : Rp %.2f\n', harga_per_kg(1));
    fprintf('2. Telur  : Rp %.2f\n', harga_per_kg(2));
    fprintf('3. Tepung : Rp %.2f\n', harga_per_kg(3));
    fprintf('4. Ayam   : Rp %.2f\n', harga_per_kg(4));
end
