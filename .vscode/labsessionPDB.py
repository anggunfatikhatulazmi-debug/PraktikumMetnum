import math

# =====================================================
# PDB : dy/dx = x*sqrt(y),  y(0)=1,  h=0.1
# =====================================================
def f(x, y):
    return x * math.sqrt(y)

def eksak(x):                       # hasil pemisahan variabel dengan y(0)=1
    return (1 + x**2 / 4) ** 2

a, A, b, h = 0, 1, 1.2, 0.1
N = round((b - a) / h)              # h = (b-a)/N  -> N = 12
print("Model masalah: y' = x*sqrt(y), y(0)=1, h =", h, ", N =", N)
print(f"Solusi eksak y(1.2) = {eksak(b):.6f}\n")

# ---------- Euler ----------
print("=== METODE EULER ===")
print(f"{'i':>2} {'x_i':>5} {'y_i':>10} {'f(x_i,y_i)':>11} {'y_i+1':>10}")
x, y = a, A
for i in range(N):
    fi = f(x, y)
    y_baru = y + h * fi
    print(f"{i:>2} {x:5.1f} {y:10.6f} {fi:11.6f} {y_baru:10.6f}")
    x, y = x + h, y_baru
y_euler = y

# ---------- Heun ----------
print("\n=== METODE HEUN (RK2) ===")
print(f"{'i':>2} {'x_i':>5} {'y_i':>10} {'k1':>10} {'k2':>10} {'y_i+1':>10}")
x, y = a, A
for i in range(N):
    k1 = f(x, y)
    k2 = f(x + h, y + h * k1)
    y_baru = y + h / 2 * (k1 + k2)
    print(f"{i:>2} {x:5.1f} {y:10.6f} {k1:10.6f} {k2:10.6f} {y_baru:10.6f}")
    x, y = x + h, y_baru
y_heun = y

# ---------- RK4 ----------
print("\n=== METODE RUNGE-KUTTA ORDE-4 ===")
print(f"{'i':>2} {'x_i':>5} {'y_i':>10} {'k1':>9} {'k2':>9} {'k3':>9} {'k4':>9} {'y_i+1':>10}")
x, y = a, A
for i in range(N):
    k1 = f(x, y)
    k2 = f(x + h/2, y + k1*h/2)
    k3 = f(x + h/2, y + k2*h/2)
    k4 = f(x + h,   y + k3*h)
    y_baru = y + h/6 * (k1 + 2*k2 + 2*k3 + k4)
    print(f"{i:>2} {x:5.1f} {y:10.6f} {k1:9.6f} {k2:9.6f} {k3:9.6f} {k4:9.6f} {y_baru:10.6f}")
    x, y = x + h, y_baru
y_rk4 = y

# ---------- Galat ----------
print("\n=== GALAT DI x = 1.2 ===")
print(f"{'Metode':<10} {'y(1.2)':>10} {'Galat abs':>12} {'Galat rel (%)':>14} {'< 0.0001?':>10}")
y_e = eksak(b)
print(f"{'Eksak':<10} {y_e:10.6f}")
for nama, nilai in [("Euler", y_euler), ("Heun", y_heun), ("RK4", y_rk4)]:
    ga = abs(y_e - nilai)
    gr = ga / abs(y_e) * 100
    print(f"{nama:<10} {nilai:10.6f} {ga:12.3e} {gr:14.5f} {'Ya' if ga < 1e-4 else 'Tidak':>10}")