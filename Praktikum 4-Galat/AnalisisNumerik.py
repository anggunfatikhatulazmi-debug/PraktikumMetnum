import math

class AnalisisNumerik:
    def __init__(self):
        pass

    def hitung_soal_1(self):
        print("--- SOAL 1: Perhitungan e^(0.3) dengan Deret Taylor ---")
        x = 0.3
        eksak = math.exp(x)
        print(f"Nilai Eksak = {eksak:.12f}\n")
        
        f_hampiran = 0
        for n in range(5):
            f_hampiran += (x**n) / math.factorial(n)
            E_a = abs(eksak - f_hampiran)
            E_r = (E_a / eksak) * 100
            print(f"n = {n} | Hampiran: {f_hampiran:.12f} | Ea: {E_a:.12f} | Er: {E_r:.4f}%")
        print()

    def hitung_soal_2(self):
        print("--- SOAL 2: Deret Harmonik ---")
        # a. Perhitungan Eksak
        S_a = sum(1 / i for i in range(1, 21))
        
        # b. Masing-masing pembagian dibulatkan (4 desimal)
        S_b = sum(round(1 / i, 4) for i in range(1, 21))
        
        # c. Tanpa looping (menggunakan fungsi sum)
        S_c = sum([1 / i for i in range(1, 21)])

        print(f"a. Eksak            : {S_a:.12f}")
        print(f"b. Dibulatkan (4 des): {S_b:.12f} | Ea: {abs(S_a - S_b):.12f}")
        print(f"c. Tanpa Loop (sum) : {S_c:.12f} | Ea: {abs(S_a - S_c):.12f}")
        print()

    def hitung_soal_3(self):
        print("--- SOAL 3: Perhitungan sin(1) dengan Deret Taylor ---")
        x = 1.0
        eksak = math.sin(x)
        print(f"Nilai Eksak = {eksak:.12f}\n")
        
        # Penanganan N = 1..5 sesuai indeks jumlah suku (N)
        for N in range(1, 6):
            f_hampiran = 0
            # Suku deret Taylor sin(x) dihitung dari n = 0 sampai N-1
            for n in range(N):
                suku = ((-1)**n) * (x**(2*n + 1)) / math.factorial(2*n + 1)
                f_hampiran += suku
            
            E_a = abs(eksak - f_hampiran)
            E_r = (E_a / eksak) * 100
            print(f"N = {N} | Hampiran: {f_hampiran:.12f} | Ea: {E_a:.12f} | Er: {E_r:.6f}%")
        print()

if __name__ == "__main__":
    app = AnalisisNumerik()
    app.hitung_soal_1()
    app.hitung_soal_2()
    app.hitung_soal_3()