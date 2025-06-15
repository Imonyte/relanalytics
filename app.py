import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from rela_core import compute_voltage, compute_semantic_current, assign_modulus

# Page config
st.set_page_config(layout="wide", page_title="RELAnalytics")

# Branding
st.title("🌀 RELAnalytics")
st.image("relanalytics_logo.png", use_column_width=True)
st.markdown("**Recursive Entangled Logic Engine for Semantic Fields**")

# Sidebar controls
st.sidebar.header("📂 Load Data")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
load_demo = st.sidebar.button("🧪 Load Recursive Demo")

view_mode = st.sidebar.radio("🔁 View Mode", ["Line View", "Spiral 2D", "Spiral 3D"])
mod_min = st.sidebar.slider("Min Modulus", 0, 10000, 0)
mod_max = st.sidebar.slider("Max Modulus", 100, 10000, 10000)

df = None

# Load data
if load_demo:
    demo_path = "recursive_field_demo.csv"
    if os.path.exists(demo_path):
        df = pd.read_csv(demo_path)
        st.success("✅ Loaded recursive demo dataset.")
    else:
        st.error("❌ Demo file not found.")
elif uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully.")

# Processing logic
if df is not None:
    if "distance" in df.columns and "label" in df.columns:

        # RELA core fields
        df["voltage"] = df["distance"].apply(compute_voltage)
        df["modulus"] = df["label"].apply(assign_modulus)
        df["semantic_current"] = compute_semantic_current(df["voltage"])

        # Filter by modulus range
        df = df[(df["modulus"] >= mod_min) & (df["modulus"] <= mod_max)]

        # Metrics
        st.subheader("📊 RELAnalytics Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", len(df))
        col2.metric("Unique Labels", df['label'].nunique())
        col3.metric("ΔV Average", round(df["semantic_current"].abs().mean(), 5))

        # Visualization
        if view_mode == "Line View":
            st.line_chart(df[["voltage", "semantic_current"]])
            st.bar_chart(df["modulus"])

        elif view_mode == "Spiral 2D":
            st.subheader("🌐 Spiral Voltage Field (2D)")
            fig = plt.figure(figsize=(7, 7))
            ax = fig.add_subplot(111, polar=True)

            theta = np.linspace(0, 2 * np.pi, len(df))
            radius = df["voltage"]
            colors = df["modulus"]

            scatter = ax.scatter(theta, radius, c=colors, cmap='plasma', s=30, alpha=0.9)
            cbar = fig.colorbar(scatter, ax=ax, orientation='vertical', pad=0.1)
            cbar.set_label('Modulus (Phase)')

            harmonic_rings = [100, 500, 1000, 5000, 10000]
            for hr in harmonic_rings:
                ring_r = 1 / (hr + 0.1)
                ax.plot(np.linspace(0, 2*np.pi, 200), [ring_r]*200, '--', color='grey', linewidth=0.7, alpha=0.6)
                ax.text(0, ring_r + 0.002, f'{hr}', fontsize=8, ha='center', color='grey')

            ax.set_title("Recursive Spiral Voltage Field", va='bottom')
            st.pyplot(fig)

        elif view_mode == "Spiral 3D":
            st.subheader("🔺 3D Spiral Voltage Field")

            theta = np.linspace(0, 4 * np.pi, len(df))
            r = df["voltage"]
            z = df["semantic_current"]
            color = df["modulus"]

            x = r * np.cos(theta)
            y = r * np.sin(theta)

            fig = go.Figure(data=go.Scatter3d(
                x=x, y=y, z=z,
                mode='markers+lines',
                marker=dict(
                    size=4,
                    color=color,
                    colorscale='Viridis',
                    colorbar=dict(title="Modulus"),
                    opacity=0.8
                ),
                line=dict(color='rgba(50,50,200,0.2)', width=1)
            ))

            fig.update_layout(
                height=700,
                margin=dict(l=0, r=0, b=0, t=30),
                scene=dict(
                    xaxis_title='X (cos θ)',
                    yaxis_title='Y (sin θ)',
                    zaxis_title='ΔV (Semantic Current)',
                    bgcolor='white'
                ),
                title="Recursive 3D Spiral View"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Show data table
        st.dataframe(df.head(30))

        # Download processed data
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Processed CSV", csv, "processed_data.csv", "text/csv")

    else:
        st.warning("⚠️ CSV must contain 'distance' and 'label' columns.")
else:
    st.info("Upload a file or click 'Load Recursive Demo' to begin.")
