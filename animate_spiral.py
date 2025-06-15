import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import imageio
from tqdm import tqdm

# Load your RELAnalytics CSV
CSV_PATH = "recursive_field_demo.csv"  # or any processed file
df = pd.read_csv(CSV_PATH)

# Compute spiral fields
df["voltage"] = 1 / (df["distance"] + 0.1)
df["semantic_current"] = df["voltage"].diff().fillna(0)
df["modulus"] = df["label"].map({
    "pedestrian": 500,
    "car": 5000,
    "zone": 100,
    "crosswalk": 1000,
    "stop": 200
}).fillna(500)

# Spiral coordinates
theta = np.linspace(0, 4 * np.pi, len(df))
r = df["voltage"]
z = df["semantic_current"]
color = df["modulus"]
x = r * np.cos(theta)
y = r * np.sin(theta)

# Create output folder
FRAME_DIR = "spiral_frames"
os.makedirs(FRAME_DIR, exist_ok=True)

# Render frames
print("🔁 Generating spiral frames...")
for i in tqdm(range(10, len(df), 5)):
    fig = go.Figure(data=go.Scatter3d(
        x=x[:i], y=y[:i], z=z[:i],
        mode='lines+markers',
        marker=dict(
            size=4,
            color=color[:i],
            colorscale='Viridis',
            opacity=0.8
        ),
        line=dict(color='rgba(50,50,200,0.3)', width=2)
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='cos θ',
            yaxis_title='sin θ',
            zaxis_title='ΔV',
            bgcolor='white'
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        title=f"RELA Spiral Frame {i}"
    )

    frame_path = os.path.join(FRAME_DIR, f"frame_{i:04}.png")
    fig.write_image(frame_path, engine="kaleido")

# Assemble GIF
print("🎞 Assembling GIF...")
images = [imageio.imread(os.path.join(FRAME_DIR, f)) for f in sorted(os.listdir(FRAME_DIR)) if f.endswith(".png")]
imageio.mimsave("spiral_animation.gif", images, duration=0.1)
print("✅ Saved: spiral_animation.gif")

# Optional: MP4 export
try:
    imageio.mimsave("spiral_animation.mp4", images, fps=10)
    print("✅ Saved: spiral_animation.mp4")
except Exception as e:
    print("⚠️ Could not export MP4:", e)
