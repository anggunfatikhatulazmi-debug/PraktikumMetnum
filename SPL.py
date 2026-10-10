import time
import numpy as np

# --- DEFINISI SISTEM PERSAMAAN LINIER (SPL) ---
# 1)  5p -  q -  r            = -1
# 2) -p + 5q -  r -  s      =  2
# 3) -p -  q + 4r -  s -  t =  6
# 4)             r + 4s - 2t =  2
# 5)      q -  r +  s + 4t = -1

A = np.array([
    [ 5, -1, -1,  0,  0],
    [-1,  5, -1, -1,  0],
    [-1, -1,  4, -1, -1],
    [ 0,  0,  1,  4, -2],
    [ 0,  1, -1,  1,  4]
], dtype=float)

b = np.array([-1, 2, 6, 2, -1], dtype=float)

MAX_ITER = 20       # Batas maksimum iterasi
TOLERANSI = 0.001   # Batas toleransi error
n = len(b)


# ==========================================
# 1. METODE ELIMINASI GAUSS
# ==========================================
def metode_gauss(A, b):
    start = time.perf_counter()
    Aug = np.hstack((A, b.reshape(-1, 1)))
    
    for i in range(n):
        max_row = i + np.argmax(np.abs(Aug[i:, i]))
        Aug[[i, max_row]] = Aug[[max_row, i]]
        for j in range(i + 1, n):
            factor = Aug[j, i] / Aug[i, i]
            Aug[j, i:] -= factor * Aug[i, i:]
            
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Aug[i, -1] - np.dot(Aug[i, i + 1:n], x[i + 1:n])) / Aug[i, i]
        
    return x, time.perf_counter() - start


# ==========================================
# 2. METODE GAUSS-JORDAN
# ==========================================
def metode_gauss_jordan(A, b):
    start = time.perf_counter()
    Aug = np.hstack((A, b.reshape(-1, 1)))
    
    for i in range(n):
        max_row = i + np.argmax(np.abs(Aug[i:, i]))
        Aug[[i, max_row]] = Aug[[max_row, i]]
        Aug[i] = Aug[i] / Aug[i, i]
        for j in range(n):
            if j != i:
                factor = Aug[j, i]
                Aug[j] -= factor * Aug[i]
                
    return Aug[:, -1], time.perf_counter() - start


# ==========================================
# 3. METODE DEKOMPOSISI LU (Manual NumPy)
# ==========================================
def metode_dekomposisi_lu(A, b):
    start = time.perf_counter()
    n = len(b)
    L = np.eye(n)
    U = A.copy()
    
    for i in range(n):
        for j in range(i + 1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
            
    # Penyelesaian L * y = b (Forward substitution)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - np.dot(L[i, :i], y[:i])
        
    # Penyelesaian U * x = y (Backward substitution)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]
        
    return x, time.perf_counter() - start


# ==========================================
# 4. METODE ITERASI JACOBI
# ==========================================
def metode_jacobi(A, b, nilai_eksak):
    start = time.perf_counter()
    x = np.zeros(n)
    iterasi = 0
    galat = float('inf')
    
    while iterasi < MAX_ITER and galat > TOLERANSI:
        x_new = np.zeros(n)
        for i in range(n):
            s = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
            
        galat = np.max(np.abs(nilai_eksak - x_new))
        x = x_new
        iterasi += 1
        
    return x, iterasi, galat, time.perf_counter() - start


# ==========================================
# 5. METODE ITERASI GAUSS-SEIDEL
# ==========================================
def metode_gauss_seidel(A, b, nilai_eksak):
    start = time.perf_counter()
    x = np.zeros(n)
    iterasi = 0
    galat = float('inf')
    
    while iterasi < MAX_ITER and galat > TOLERANSI:
        x_new = x.copy()
        for i in range(n):
            s = sum(A[i, j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i, i]
            
        galat = np.max(np.abs(nilai_eksak - x_new))
        x = x_new
        iterasi += 1
        
    return x, iterasi, galat, time.perf_counter() - start


# ==========================================
# EKSEKUSI UTAMA & OUTPUT
# ==========================================
if __name__ == "__main__":
    # Menggunakan Gauss-Jordan sebagai referensi nilai eksak untuk perhitungan galat
    nilai_eksak_acuan, _ = metode_gauss_jordan(A, b)

    x_gauss, t_gauss = metode_gauss(A, b)
    x_gj, t_gj = metode_gauss_jordan(A, b)
    x_lu, t_lu = metode_dekomposisi_lu(A, b)
    x_jacobi, iter_jacobi, galat_jacobi, t_jacobi = metode_jacobi(A, b, nilai_eksak_acuan)
    x_seidel, iter_seidel, galat_seidel, t_seidel = metode_gauss_seidel(A, b, nilai_eksak_acuan)

    print("=" * 60)
    print("                 HASIL PENYELESAIAN SPL")
    print("=" * 60)
    print(f"1. Gauss         : {np.round(x_gauss, 4)}")
    print(f"2. Gauss-Jordan  : {np.round(x_gj, 4)}")
    print(f"3. Dekomposisi LU: {np.round(x_lu, 4)}")
    print(f"4. Jacobi        : {np.round(x_jacobi, 4)}  (Iterasi: {iter_jacobi})")
    print(f"5. Gauss-Seidel  : {np.round(x_seidel, 4)}  (Iterasi: {iter_seidel})")

    print("\n" + "=" * 60)
    print("                 ANALISIS GALAT ABSTRAK")
    print("=" * 60)
    print(f"Galat Metode Jacobi        : {galat_jacobi:.6f}")
    print(f"Galat Metode Gauss-Seidel  : {galat_seidel:.6f}")

    print("\n" + "=" * 60)
    print("                 RUNNING TIME")
    print("=" * 60)
    print(f"Waktu Gauss          : {t_gauss:.8f} detik")
    print(f"Waktu Gauss-Jordan   : {t_gj:.8f} detik")
    print(f"Waktu Dekomposisi LU : {t_lu:.8f} detik")
    print(f"Waktu Jacobi         : {t_jacobi:.8f} detik")
    print(f"Waktu Gauss-Seidel   : {t_seidel:.8f} detik")
    print("=" * 60)