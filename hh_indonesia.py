
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# ====================================================================
# Hodgkin-Huxley Indonesia 2025 – Gold Standard with Corrected h-gate
# ====================================================================

CM = 1.0; ENA = 50.0; EK = -77.0; EL = -54.4
GNA_BAR = 120.0; GK_BAR = 36.0; GL_BAR = 0.3
PHI = 1.0

def alpha_m(V): return PHI * 0.1 * (25 - V) / (np.exp((25 - V)/10) - 1) if abs(V-25)>1e-8 else PHI*1.0
def beta_m(V):  return PHI * 4.0 * np.exp(-V/18)

def alpha_h(V): return PHI * 1.0 / (np.exp((30 - V)/10) + 1)          # CORRECTED: inactivation
def beta_h(V):  return PHI * 0.07 * np.exp(-V/20)                    # CORRECTED

def alpha_n(V): return PHI * 0.01 * (10 - V) / (np.exp((10 - V)/10) - 1) if abs(V-10)>1e-8 else PHI*0.1
def beta_n(V):  return PHI * 0.125 * np.exp(-V/80)

def x_inf(a, b): return a / (a + b)

def I_stim(t, amplitude=10.0, t_on=10.0, duration=20.0):
    return amplitude if t_on <= t < t_on + duration else 0.0

def rhs(t, y):
    V, m, h, n = y
    INa = GNA_BAR * m**3 * h * (V - ENA)
    IK  = GK_BAR * n**4 * (V - EK)
    IL  = GL_BAR * (V - EL)
    dVdt = (I_stim(t) - (INa + IK + IL)) / CM
    dmdt = alpha_m(V)*(1-m) - beta_m(V)*m
    dhdt = alpha_h(V)*(1-h) - beta_h(V)*h
    dndt = alpha_n(V)*(1-n) - beta_n(V)*n
    return [dVdt, dmdt, dhdt, dndt]

# ====================================================================
# Run both conditions
# ====================================================================

def simulate_and_plot(V(v_rest, label, color):
    y0 = [v_rest,
          x_inf(alpha_m(v_rest), beta_m(v_rest)),
          x_inf(alpha_h(v_rest), beta_h(v_rest)),
          x_inf(alpha_n(v_rest), beta_n(v_rest))]
    
    sol = solve_ivp(rhs, [0, 100], y0, method='BDF', t_eval=np.linspace(0, 100, 10000))
    
    print(f"\n--- {label} (V_rest = {v_rest} mV) ---")
    print(f"h₀ = {y0[2]:.6f}")
    print(f"Peak V = {sol.y[0].max():.2f} mV")
    
    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    plt.plot(sol.t, sol.y[0], color=color, lw=2)
    plt.title(f'Hodgkin-Huxley Indonesia 2025 – {label}')
    plt.ylabel('Membrane Potential (mV)')
    plt.axvline(10, color='red', linestyle='--', alpha=0.5)
    plt.axvline(30, color='red', linestyle='--', alpha=0.5)
    
    plt.subplot(2,1,2)
    plt.plot(sol.t, sol.y[2], color='orange', lw=2)
    plt.ylabel('h (Na inactivation)')
    plt.xlabel('Time (ms)')
    plt.tight_layout()
    
    os.makedirs("results", exist_ok=True)
    plt.savefig(f"results/{'normal' if v_rest==-65 else 'depolarized'}_block.png", dpi=200)
    plt.show()

# NORMAL RESTING POTENTIAL
simulate_and_plot(-65, "Normal Resting Potential", "darkblue")

# DEPOLARIZED → TRUE DEPOLARIZATION BLOCK
simulate_and_plot(-40, "Depolarized – True Inactivation Block", "darkred")
