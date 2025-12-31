import numpy as np
import warnings

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def LiTaO3(x):
    """
    Material model for: LiTaO3 (ordinary refractive index no)

    Optical transparency window: 0.45 um – 4.00 um

    INPUT:
        x - wavelength (micron), scalar or array-like

    OUTPUT:
        n - refractive index (numpy array)
    """
    x = np.asarray(x, dtype=float)

    # transparency window check
    if np.any((x < 0.45) | (x > 4.00)):
        warnings.warn(
            "Extrapolating Sellmeier equation for LiTaO3 beyond "
            "optical transparency window of 0.45 um – 4.00 um",
            RuntimeWarning
        )

    A1 = 4.51224
    A2 = 0.0847522
    A3 = 0.19876
    A4 = -0.0239046

    n = np.sqrt(A1 + A2 / (x**2 - A3**2) + A4 * x**2)
    return n

# 测试代码
lambda_um = np.linspace(0.5, 2.0, 1501)
n = LiTaO3(lambda_um)

plt.plot(lambda_um, n)
plt.xlabel("Wavelength (µm)")
plt.ylabel("Refractive index")
plt.grid(True)
plt.show()

print(LiTaO3(1.55))