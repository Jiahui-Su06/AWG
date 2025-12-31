import numpy as np
import warnings

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def SiO2(x):
    """
    Sellmeier model for SiO2 (Fused Silica) at 20°C
    Valid wavelength range: 0.21 µm – 6.7 µm

    Parameters
    ----------
    x : float or array_like
        Wavelength(s) in micrometers (µm)

    Returns
    -------
    n : float or ndarray
        Refractive index
    """
    x = np.asarray(x, dtype=float)  # 支持标量和数组

    # 检查波长范围
    if np.any(x < 0.21) or np.any(x > 6.7):
        warnings.warn("Extrapolating Sellmeier equation for SiO2 beyond range of 0.21–6.7 µm", UserWarning)

    # Sellmeier 方程
    n = np.sqrt(
        1
        + 0.6961663 / (1 - (0.0684043 / x) ** 2)
        + 0.4079426 / (1 - (0.1162414 / x) ** 2)
        + 0.8974794 / (1 - (9.8961610 / x) ** 2)
    )

    # 如果输入是标量，返回标量
    if n.size == 1:
        return n.item()
    return n

# 测试代码
lambda_um = np.linspace(0.5, 0.9, 401)
n = SiO2(lambda_um)

plt.plot(lambda_um, n)
plt.xlabel("Wavelength (µm)")
plt.ylabel("Refractive index")
plt.grid(True)
plt.show()

print(SiO2(0.6))
