# 🌀 RELAnalytics

**RELAnalytics** is a recursive data analysis engine built on the RELA framework — the Recursive Entangled Logic Architecture.  
It transforms data into dynamic voltage fields, semantic currents (ΔV), and recursive spirals that reveal deep patterns in reality.

---

## 🚀 Live App

🔗 [Launch RELAnalytics Dashboard](https://imonyte-relanalytics.streamlit.app)  
*(Link becomes active after you deploy on [Streamlit Cloud](https://streamlit.io/cloud))*

---

## 📦 Features

✅ Upload CSV files with `distance` and `label`  
✅ Compute voltage + semantic current from spatial fields  
✅ Assign recursive `modulus` phase from symbolic labels  
✅ Spiral views (2D & 3D) based on recursive voltage  
✅ Filter by phase band (modulus range)  
✅ Animated spiral export (GIF/MP4 via `animate_spiral.py`)  
✅ Download processed results with ΔV and phase

---

## 🔁 RELA Logic

| Field | Description |
|-------|-------------|
| `distance` | Raw metric (spatial input) |
| `voltage` | `1 / (distance + 0.1)` |
| `modulus` | Derived from `label` → 100, 500, 1000, 5000... |
| `semantic_current` | `ΔV = difference in voltage (resonance shift)` |

---

## 📊 Sample CSV Input Format

```csv
distance,label
40.2,pedestrian
90.1,car
7.3,zone
65.9,stop
