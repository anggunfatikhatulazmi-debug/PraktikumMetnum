import numpy as np

def gauss_jordan(A, b):
    n = len(b)
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    for i in range(n):
        # Normalisasi baris i agar elemen diagonal menjadi 1
        M[i] = M[i] / M[i, i]
        
        # Eliminasi elemen pada kolom i di semua baris lainnya
        for j in range(n):
            if i != j:
                factor = M[j, i]
                M[j] -= factor * M[i]
                
    return M[:, -1]

# Input Data
A = np.array([[2, 1, -1],
              [4, 3, 1],
              [-2, 1, 2]], dtype=float)
b = np.array([3, 9, 4], dtype=float)

x = gauss_jordan(A, b)
print("=== Metode Eliminasi Gauss-Jordan ===")
print(f"x1 = {x[0]:.2f}, x2 = {x[1]:.2f}, x3 = {x[2]:.2f}")