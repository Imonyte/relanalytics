import numpy as np

def compute_voltage(distance):
    """Convert distance into a voltage value for RELA logic."""
    return 1 / (distance + 0.1)  # Prevent divide-by-zero

def compute_semantic_current(voltage_series):
    """Compute the semantic current (ΔV) as difference in voltage."""
    return voltage_series.diff().fillna(0)

def assign_modulus(label):
    """Assign modulus value based on label for recursive phase logic."""
    label = str(label).lower()
    if 'crosswalk' in label:
        return 1000
    elif 'zone' in label:
        return 100
    elif 'car' in label:
        return 5000
    elif 'stop' in label:
        return 200
    else:
        return 500  # default (e.g. pedestrian)
