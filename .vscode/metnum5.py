import numpy as np

def gauss_elimination(A, b):
    n = len(b)
    # Membuat augmented matrix [A|b]
    M = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    # Forward Elimination
    for i in range(n):
        for j in range(i + 1, n):
            factor = M[j, i] / M[i, i]
            M[j, i:] -= factor * M[i, i:]
            
    # Backward Substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (M[i, -1] - np.dot(M[i, i+1:n], x[i+1:n])) / M[i, i]
        
    return x

# Input Data
A = np.array([[2, 1, -1],
              [4, 3, 1],
              [-2, 1, 2]], dtype=float)
b = np.array([3, 9, 4], dtype=float)

x = gauss_elimination(A, b)
print("=== Metode Eliminasi Gauss ===")
print(f"x1 = {x[0]:.2f}, x2 = {x[1]:.2f}, x3 = {x[2]:.2f}")