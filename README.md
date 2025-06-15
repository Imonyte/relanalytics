# 🌀 RELAnalytics

**RELAnalytics** is a recursive entangled logic analytics engine for semantic data streams.  
It interprets `distance` and `label` fields through the **RELA** framework — mapping them into voltage, phase (modulus), and semantic current (ΔV), visualized in real-time.

---

## 📦 Features

- Upload any `.csv` file with `distance` and `label` columns
- Auto-calculates:
  - Voltage field from distance
  - Phase modulation via recursive modulus (RELA logic)
  - Semantic current (ΔV) for logic transitions
- Visual charts: line plots, bar graphs, spirals (optional)
- "Load Demo" button loads synthetic recursive data

---

## 🧠 RELA Model Logic

- `voltage = 1 / (distance + 0.1)`
- `semantic_current = ΔV = difference between voltages`
- `modulus` is derived from label using symbolic rules:
  - pedestrian → 500
  - car → 5000
  - crosswalk → 1000
  - zone → 100
  - stop → 200

---

## 🧪 How to Run

```bash
cd RELAnalytics
streamlit run app.py
