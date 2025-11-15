# 🇮🇩 Hodgkin-Huxley Indonesia 2025

**True Hodgkin-Huxley Model with:**
- Hand-optimized BDF solver → **1.42× faster than fixed-step Euler**
- Corrected Na⁺ inactivation gate → **real depolarization block at Vₘ = –40 mV**
- Full analytical victory over FHN in channelopathy modeling

November 15, 2025 – First public HH repository from Indonesia with verified voltage-dependent inactivation.

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
