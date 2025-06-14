import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
from io import StringIO
from rela_core import run_rela_pipeline

# Set up page
st.set_page_config(page_title="RELAnalytics", layout="centered")

st.title("🌀 RELAnalytics")
# Load and display the logo
logo = Image.open("relanalytics_logo.png")
st.image(logo, width=220)

# Branding welcome message
st.markdown("## 🔍 Welcome to RELAnalytics")
st.markdown("""
**RELAnalytics** is a recursive-entangled logic field platform  
designed to extract meaning from structured spatial-semantic data.

Upload your CSV to begin analyzing recursive voltage fields, semantic current,  
and modulus-phase rings in real time.
""")
st.subheader("Recursive Entangled Logic Field Visualizer")
st.markdown("Upload a CSV with at least `distance` and `label` columns.")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Run RELA logic
        df = run_rela_pipeline(uploaded_file)
        st.success("✅ Data processed with RELA core logic.")

        # Filter by label
        unique_labels = df['label'].unique()
        selected_labels = st.multiselect("🔍 Filter by label:", unique_labels, default=list(unique_labels))
        filtered_df = df[df['label'].isin(selected_labels)]

        st.markdown("### 🔍 Filtered RELA Data Preview:")
        st.dataframe(filtered_df.head(10))

        # 📊 Summary Metrics
        if not filtered_df.empty:
            col1, col2, col3 = st.columns(3)
            col1.metric("⚡ Avg Voltage", f"{filtered_df['voltage'].mean():.2f} V")
            col2.metric("ΔV (Peak)", f"{filtered_df['semantic_current'].max():.2f}")
            col3.metric("🌀 Phases", f"{filtered_df['modulus'].nunique()}")
        else:
            st.warning("No data to summarize — please check your filters or CSV.")

        # 📈 Voltage over Time
        st.markdown("### ⚡ Voltage Over Time")
        fig1, ax1 = plt.subplots()
        ax1.plot(filtered_df.index, filtered_df['voltage'], label='Voltage', color='blue')
        ax1.set_ylabel("Voltage (V)")
        ax1.set_xlabel("Time Index")
        ax1.legend()
        st.pyplot(fig1)

        # 🧠 Semantic Current (ΔV)
        st.markdown("### 🧠 Semantic Current (ΔV)")
        fig2, ax2 = plt.subplots()
        sns.lineplot(x=filtered_df.index, y=filtered_df['semantic_current'], ax=ax2, color='orange')
        ax2.set_ylabel("Current")
        ax2.set_xlabel("Time Index")
        st.pyplot(fig2)

        # 🌀 Phase Ring Mapping
        st.markdown("### 🌀 Phase Ring Mapping")
        st.bar_chart(filtered_df['modulus'])

        # 🌌 Semantic Spiral
        st.markdown("### 🌌 Semantic Spiral of Voltage-Phase Field")
        try:
            spiral_df = filtered_df.copy()
            angles = np.linspace(0, 2 * np.pi, len(spiral_df))
            radius = spiral_df['voltage']

            fig_spiral = plt.figure(figsize=(6, 6))
            ax = fig_spiral.add_subplot(111, polar=True)
            ax.plot(angles, radius, marker='o', color='purple', linewidth=2)
            ax.set_title("Semantic Spiral: Voltage Resonance Field", va='bottom')
            st.pyplot(fig_spiral)
        except Exception as spiral_error:
            st.warning(f"⚠️ Spiral could not be plotted: {spiral_error}")

        # 💾 Download CSV
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Download Processed CSV",
            data=csv_data,
            file_name='rela_processed.csv',
            mime='text/csv'
        )

        # 🔗 Placeholder: Real-Time Data Integration
        st.markdown("### 🔌 Live Sensor API Integration")
        st.info("This module is ready to connect to camera/LiDAR or traffic APIs. Future builds will include stream-based ingestion.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
else:
    st.warning("📎 Please upload a CSV file to begin analysis.")
