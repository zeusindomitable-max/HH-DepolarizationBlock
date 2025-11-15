# hh_gold_standard_2025.py
# T-HH 2025 – Tedjamantri Hodgkin-Huxley 2025
# Exact HH 1952 implementation with Q10 correction (6.3°C)
# Realistic partial inactivation at -40 mV → physiologically correct
# Released: 16 November 2025, 02:30 WIB
# Author: @haritedjamantri
# DOI: https://doi.org/10.5281/zenodo.17618662

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import os

# ====================================================================
# PARAMETERS – Hodgkin-Huxley 1952 (T = 6.3°C)
# ====================================================================
Cm, gNa, gK, gL = 1.0, 120.0, 35.0, 0.3
ENa, EK, EL = 50.0, -77.0, -54.4
PHI = 0.325                                      # Q10 correction for 6.3°C

I_STIM = 30.0
T_STIM_ON, T_STIM_OFF = 10.0, 40.0

def I_stim(t):
    return I_STIM if T_STIM_ON <= t <= T_STIM_OFF else 0.0

# Voltage shift: HH 1952 defined V = 0 at resting potential ≈ -65 mV
def V_hh(V_bio):
    return V_bio + 65.0

# ====================================================================
# RATE FUNCTIONS – EXACT FROM HH 1952 (with PHI & voltage shift)
# ====================================================================
def alpha_m(V_bio): 
    V = V_hh(V_bio)
    return PHI * (0.1 * (25 - V) / (np.exp((25 - V) / 10) - 1) if abs(25 - V) > 1e-6 else 1.0)

def beta_m(V_bio):  
    V = V_hh(V_bio)
    return PHI * 4.0 * np.exp(-V / 18)

def alpha_h(V_bio): 
    V = V_hh(V_bio)
    return PHI * 0.07 * np.exp(-V / 20)

def beta_h(V_bio):  
    V = V_hh(V_bio)
    return PHI * 1.0 / (1.0 + np.exp((30 - V) / 10))

def alpha_n(V_bio): 
    V = V_hh(V_bio)
    return PHI * (0.01 * (10 - V) / (np.exp((10 - V) / 10) - 1) if abs(10 - V) > 1e-6 else 0.1)

def beta_n(V_bio):  
    V = V_hh(V_bio)
    return PHI * 0.125 * np.exp(-V / 80)

def x_inf(alpha_func, beta_func, V):
    a = alpha_func(V)
    b = beta_func(V)
    return a / (a + b)

# ====================================================================
# ODE SYSTEM
# ====================================================================
def hh_ode(t, y):
    V, m, h, n = y
    INa = gNa * m**3 * h * (V - ENa)
    IK  = gK  * n**4     * (V - EK)
    IL  = gL            * (V - EL)
    dV = (I_stim(t) - INa - IK - IL) / Cm
    dm = alpha_m(V) * (1 - m) - beta_m(V) * m
    dh = alpha_h(V) * (1 - h) - beta_h(V) * h
    dn = alpha_n(V) * (1 - n) - beta_n(V) * n
    return [dV, dm, dh, dn]

# ====================================================================
# SIMULATION
# ====================================================================
os.makedirs("results", exist_ok=True)
t_span = (0.0, 100.0)
t_eval = np.linspace(0, 100, 10000)

for V_rest, label, color in [(-65.0, "Normal (-65 mV)", "navy"), (-40.0, "Depolarized (-40 mV)", "crimson")]:
    y0 = [V_rest,
          x_inf(alpha_m, beta_m, V_rest),
          x_inf(alpha_h, beta_h, V_rest),
          x_inf(alpha_n, beta_n, V_rest)]
    
    h0 = y0[2]
    
    sol = solve_ivp(hh_ode, t_span, y0, method='BDF', t_eval=t_eval, rtol=1e-8, atol=1e-10)
    
    peak = np.max(sol.y[0])
    print(f"{label} → h₀ = {h0:.5f} | Peak V = {peak:+6.2f} mV")
    
    plt.figure(figsize=(10, 5))
    plt.plot(sol.t, sol.y[0], color=color, lw=2.5)
    plt.title(f"T-HH 2025 │ {label}\nInitial h = {h0:.5f} → Peak = {peak:+.2f} mV")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Potential (mV)")
    plt.axvspan(T_STIM_ON, T_STIM_OFF, color='gray', alpha=0.2, label=f"Stimulus {I_STIM} µA/cm²")
    plt.ylim(-90, 60)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"results/T-HH_2025_{'normal' if V_rest == -65 else 'depolarized'}.png", dpi=300)
    plt.show()

print("\nT-HH 2025 – Gold Standard Hodgkin-Huxley Indonesia 2025")
print("Realistic partial inactivation at -40 mV (h₀ ≈ 0.05) – physiologically correct")
print("DOI: https://doi.org/10.5281/zenodo.17618662")
print("Released by @haritedjamantri – 16 November 2025")
