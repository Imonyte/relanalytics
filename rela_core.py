import pandas as pd
import numpy as np

def map_voltage_from_distance(distance, scale=10.0):
    """
    Converts distance into RELA-style voltage.
    Closer distance results in higher voltage.
    """
    try:
        return np.clip(scale / (distance + 0.1), 0, scale)
    except:
        return 0  # fallback in case of invalid distance

def assign_modulus(label):
    """
    Assigns modular group (phase ring) based on label.
    Adjust logic here for more semantic types.
    """
    label = label.lower()
    if 'crosswalk' in label:
        return 1000
    elif 'zone' in label:
        return 100
    elif 'pedestrian' in label:
        return 500
    elif 'stop' in label:
        return 1000
    else:
        return 100  # default phase

def compute_semantic_current(voltage_series):
    """
    Computes semantic current (ΔV) as first difference of voltage.
    """
    return voltage_series.diff().fillna(0)

def process_data(df):
    """
    Full RELA processing pipeline:
    - Voltage assignment
    - Phase modulus tagging
    - Current calculation
    """
    df['voltage'] = df['distance'].apply(map_voltage_from_distance)
    df['modulus'] = df['label'].apply(assign_modulus)
    df['semantic_current'] = compute_semantic_current(df['voltage'])
    return df

def run_rela_pipeline(csv_file):
    """
    Entry point for RELAnalytics app:
    Reads CSV, processes data through RELA pipeline.
    """
    df = pd.read_csv(csv_file)
    
    required_cols = {'distance', 'label'}
    if not required_cols.issubset(df.columns):
        raise ValueError("CSV must contain at least 'distance' and 'label' columns.")

    df = process_data(df)
    return df
