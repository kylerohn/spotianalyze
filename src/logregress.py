import numpy as np


def distribution_plot_values(attribute_data: np.array):
    mean = np.mean(attribute_data)
    std = np.std(attribute_data)

    x = np.arange(np.min(attribute_data), np.max(attribute_data), std/100, dtype=float)
    y = []
    for _x in x:
        y.append(distribution_formula(_x, mean, std))
    
    return (x, np.array(y))
    
# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def distribution_formula(x: float, mean: float, std: float):
    exponent = np.power(np.e, (-0.5*((x - mean)/std) ** 2))
    fraction = 1 / (std*np.sqrt(2*np.pi))
    return exponent * fraction