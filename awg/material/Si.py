import numpy as np
import warnings

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


def Si(x, T=295):
    """
    Refractive index model for Silicon (Si) as a function of wavelength and temperature
    Valid wavelength: 1.1 – 5.6 µm
    Valid temperature: 20 – 300 K

    Parameters
    ----------
    x : float or array_like
        Wavelength(s) in micrometers (µm)
    T : float, optional
        Temperature in Kelvin (default 295 K)

    Returns
    -------
    n : float or ndarray
        Refractive index
    """
    x = np.asarray(x, dtype=float)

    # 波长范围警告
    if np.any(x < 1.1) or np.any(x > 5.6):
        warnings.warn("Extrapolating model equation for Si beyond range of 1.1–5.6 µm", UserWarning)

    # 温度范围警告
    if T < 20 or T > 300:
        warnings.warn("Extrapolating model equation for Si beyond temperature range of 20K–300K", UserWarning)

    # 多项式系数计算 S1, S2, S3, x1, x2, x3
    S1 = np.polyval([3.4469e-12, -5.823e-09, 4.2169e-06, -0.00020802, 10.491], T)
    S2 = np.polyval([-1.3509e-06, 0.0010594, -0.27872, 29.166, -1346.6], T)
    S3 = np.polyval([103.24, 678.41, -76158, -1.7621e6, 4.4283e7], T)
    x1 = np.polyval([2.3248e-14, -2.5105e-10, 1.6713e-07, -1.1423e-05, 0.29971], T)
    x2 = np.polyval([-1.1321e-06, 0.001175, -0.35796, 42.389, -3517.1], T)
    x3 = np.polyval([23.577, -39.37, -6907.4, -1.4498e5, 1.714e6], T)

    # Sellmeier 型公式
    n = np.sqrt(
        1
        + S1 * x ** 2 / (x ** 2 - x1 ** 2)
        + S2 * x ** 2 / (x ** 2 - x2 ** 2)
        + S3 * x ** 2 / (x ** 2 - x3 ** 2)
    )

    # 如果输入是标量，返回标量
    if n.size == 1:
        return n.item()
    return n

# 测试代码
lambda_um = np.linspace(1.2, 1.6, 401)
n = Si(lambda_um)

plt.plot(lambda_um, n)
plt.xlabel("Wavelength (µm)")
plt.ylabel("Refractive index")
plt.grid(True)
plt.show()


print(Si(1.55))
