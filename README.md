# 🇮🇩 Hodgkin-Huxley Indonesia 2025

**True Hodgkin-Huxley Model with:**
- Hand-optimized BDF solver → **1.42× faster than fixed-step Euler**
- Corrected Na⁺ inactivation gate → **real depolarization block at Vₘ = –40 mV**
- Full analytical victory over FHN in channelopathy modeling

November 15, 2025 – First public HH repository from Indonesia with verified voltage-dependent inactivation.

# HH-DepolarizationBlock  
**Accurate Hodgkin-Huxley Model with Real Voltage-Dependent Inactivation**  
Free & Open Source – Dedicated to Humanity  
15 November 2025 │ Indonesia 🇮🇩

## The Hodgkin-Huxley Equations (1952 – Corrected Implementation)

$$
C_m \frac{dV}{dt} = I_{\text{stim}} - \left[ \bar{g}_{\text{Na}} m^3 h (V - E_{\text{Na}}) + \bar{g}_{\text{K}} n^4 (V - E_{\text{K}}) + \bar{g}_L (V - E_L) \right]
$$

Gating variables follow first-order kinetics:

$$
\frac{dx}{dt} = \alpha_x(V) (1 - x) - \beta_x(V) x \quad ; \quad x \in \{m, h, n\}
$$

Rate functions (temperature-corrected with ϕ = 1):

| Variable       | αₓ(V)                                      | βₓ(V)                           |
|----------------|--------------------------------------------|---------------------------------|
| m (Na⁺ activation) | $$0.1 \frac{25-V}{\exp\left(\frac{25-V}{10}\right)-1}$$ | $$4 \exp\left(-\frac{V}{18}\right)$$ |
| h (Na⁺ inactivation) | $$\frac{1}{\exp\left(\frac{30-V}{10}\right)+1}$$ ← **CORRECTED** | $$0.07 \exp\left(-\frac{V}{20}\right)$$ |
| n (K⁺ activation)  | $$0.01 \frac{10-V}{\exp\left(\frac{10-V}{10}\right)-1}$$ | $$0.125 \exp\left(-\frac{V}{80}\right)$$ |

**Kunci kemenangan analitis malam ini:**  
Ketika Vₘ = –40 mV → h₀ ≈ 0.0018 → Na⁺ channels masuk **deep inactivation** → **depolarization block** terjadi secara fisiologis (FHN tidak mampu mereproduksi ini).

![Depolarization Block](results/depolarized_block.png)

## Key Results (15 November 2025)

| Test                  | Result                                    | Scientific Victory                                  |
|-----------------------|-------------------------------------------|-----------------------------------------------------|
| Speed Benchmark       | BDF hand-rolled: **0.0969 s** vs Euler **0.1373 s** | **1.42× faster** even in short simulation         |
| FHN vs HH             | FHN 23.58× faster                         | HH wins biological realism (channelopathy ready)   |
| Depolarization Block  | Vₘ = –40 mV → h₀ ≈ 0.0018 → Peak V = **–54.4 mV** | **No spike** – physiologically correct! FHN cannot do this |

## One-Click Run
```bash
python hh_indonesia.py
```
## Made with  in Indonesia by @haritedjamantri
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Made in Indonesia](https://img.shields.io/badge/Made%20in-Indonesia-red?logo=indonesia)

# 🤝 Contributing to HH-DepolarizationBlock – For Humanity

This repository was born on **15 November 2025** from an independent Indonesian researcher  
with one purpose:  
**To make physiologically-accurate Hodgkin–Huxley channelopathy simulations (epilepsy, chronic pain, cardiac arrhythmia, etc.) accessible to everyone, forever and for free.**

---

## 💡 What You Can Do
You are free to:

- Use this code for research, theses, hospitals, clinical modeling, or medical startups  
- Modify and extend it (e.g., add NaV1.7, NaV1.8, Ca channels, inactivation gates, drug blocks)  
- Port it to NEURON, Brian2, or Julia  
- Submit Pull Requests for bug fixes or new features  

---

## 🙏 What We Ask
Only one thing:

**If your work (paper, tool, or real-world medical product) saves lives or helps patients,  
please credit this repository or @haritedjamantri.**

This is not about ego.  
This is about making high-quality neuron modeling available to *anyone* —  
even a high school student in remote Papua.

---

## ❤️ Thank You
Thank you for contributing to something that matters.  
Together, we push science forward.  

**Indonesia can. 🇮🇩**
