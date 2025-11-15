
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ====================================================================
# I. Parameter dan Konstanta (HH Klasik, T=6.3°C)
# ====================================================================

# Konstanta Membran dan Ekuilibrium (mV, mS/cm², µF/cm²)
CM = 1.0  
ENA = 50.0; EK = -77.0; EL = -54.4
GNA_BAR = 120.0; GK_BAR = 36.0; GL_BAR = 0.3
T_REF = 6.3 # Suhu Referensi Asli HH

# Fungsi Stimulus Eksternal
def I_stim(t):
    """Memberikan pulsa arus 10 µA/cm² dari t=10 ms hingga t=11 ms."""
    if 10 <= t <= 11:
        return 10.0
    return 0.0

# ====================================================================
# II. Fungsi Laju Kinetik (dengan Penanganan Singularitas)
# ====================================================================

# Skala Suhu (Faktor PHI)
PHI = 1.0 # Diasumsikan T_sim = T_REF, sehingga PHI = 1.0

def alpha_m(V):
    """Laju aktivasi Na (m). Penanganan singularitas V=25."""
    if np.abs(V - 25.0) < 1e-6:
        return 1.0 * PHI 
    return PHI * 0.1 * (25.0 - V) / (np.exp((25.0 - V) / 10.0) - 1.0)

def beta_m(V):
    """Laju inaktivasi Na (m)."""
    return PHI * 4.0 * np.exp(-V / 18.0)

def alpha_h(V):
    """Laju inaktivasi Na (h)."""
    return PHI * 0.07 * np.exp(-V / 20.0)

def beta_h(V):
    """Laju inaktivasi Na (h)."""
    return PHI * 1.0 / (np.exp((30.0 - V) / 10.0) + 1.0)

def alpha_n(V):
    """Laju aktivasi K (n). Penanganan singularitas V=10."""
    if np.abs(V - 10.0) < 1e-6:
        return 0.1 * PHI 
    return PHI * 0.01 * (10.0 - V) / (np.exp((10.0 - V) / 10.0) - 1.0)

def beta_n(V):
    """Laju inaktivasi K (n)."""
    return PHI * 0.125 * np.exp(-V / 80.0)

# Fungsi Steady-State (untuk inisialisasi)
def x_inf(alpha_x, beta_x):
    return alpha_x / (alpha_x + beta_x)

# ====================================================================
# III. Sistem ODE (Right-Hand Side)
# ====================================================================

def rhs_hh_system(t, y):
    """
    Fungsi RHS sistem ODE HH: dV/dt, dm/dt, dh/dt, dn/dt.
    """
    V, m, h, n = y

    # 1. Hitung Laju
    a_m, b_m = alpha_m(V), beta_m(V)
    a_h, b_h = alpha_h(V), beta_h(V)
    a_n, b_n = alpha_n(V), beta_n(V)

    # 2. Arus Ion (Persamaan Kirchhoff)
    INa = GNA_BAR * (m**3) * h * (V - ENA)
    IK  = GK_BAR * (n**4) * (V - EK)
    IL  = GL_BAR * (V - EL)

    I_total = INa + IK + IL

    # 3. Turunan
    dVdt = (I_stim(t) - I_total) / CM
    dmdt = a_m * (1.0 - m) - b_m * m
    dhdt = a_h * (1.0 - h) - b_h * h
    dndt = a_n * (1.0 - n) - b_n * n

    return [dVdt, dmdt, dhdt, dndt]

# ====================================================================
# IV. Integrasi dan Hasil
# ====================================================================

T_START = 0.0
T_END = 50.0
T_SPAN = (T_START, T_END)
T_POINTS = np.linspace(T_START, T_END, 5000)

# Kondisi Awal (V_rest = -65.0, gating pada steady state)
V_REST = -65.0  
m0 = x_inf(alpha_m(V_REST), beta_m(V_REST))
h0 = x_inf(alpha_h(V_REST), beta_h(V_REST))
n0 = x_inf(alpha_n(V_REST), beta_n(V_REST))
Y0 = [V_REST, m0, h0, n0]

print(f"--- Uji Stabilitas Hodgkin-Huxley ---")
print(f"Kondisi Awal (V, m, h, n): [{V_REST:.2f}, {m0:.4f}, {h0:.4f}, {n0:.4f}]")
print(f"Integrator: BDF (Stiff Solver)")

# Integrasi ODE
solution = solve_ivp(
    rhs_hh_system,
    T_SPAN,
    Y0,
    method='BDF',  # Pilihan terbaik untuk sistem stiff
    t_eval=T_POINTS,
    atol=1e-6,
    rtol=1e-6
)

# ====================================================================
# V. Visualisasi Hasil
# ====================================================================

if solution.success:
    V = solution.y[0, :]
    time = solution.t

    # Periksa nilai non-fisik (NaN, Inf)
    if np.any(np.isnan(solution.y)) or np.any(np.isinf(solution.y)):
        print("\n❌ GAGAL: Hasil simulasi mengandung NaN atau Infinity.")
    else:
        print(f"\n✅ SUKSES: Simulasi stabil. {len(time)} titik data dihasilkan.")

        plt.figure(figsize=(10, 6))
        plt.plot(time, V, label='V(t) - Potensial Membran', color='darkblue', linewidth=2)
        
        # Tambahkan indikator stimulus
        I_data = np.array([I_stim(t) for t in time])
        plt.plot(time, I_data * 5 - 100, label='I_stim (10µA/cm²)', linestyle='--', color='gray') # Skalakan I_stim agar terlihat
        
        plt.title('Simulasi Potensial Aksi Model Hodgkin-Huxley (Rigor)')
        plt.xlabel('Waktu (ms)')
        plt.ylabel('Potensial Membran (mV)')
        plt.ylim(-80, 50)
        plt.grid(True, linestyle=':')
        plt.legend()
        plt.show()
else:
    print(f"\n❌ GAGAL: Integrasi numerik gagal. Pesan: {solution.message}")
