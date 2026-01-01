import numpy as np
import warnings


def Si(x, T=295):
    """
    Material model (Sellmeier) for: Si
    T range: 20 K – 300 K
    lambda range: 1.1 um – 5.6 um

    INPUT:
        x - wavelength (micron), scalar or array-like
        T - temperature (K), default = 295

    OUTPUT:
        n - refractive index (numpy array or scalar)
    """

    x = np.asarray(x, dtype=float)

    # 波长范围检查
    if np.any((x < 1.1) | (x > 5.6)):
        warnings.warn(
            "Extrapolating model equation for Si beyond range of 1.1 um – 5.6 um",
            RuntimeWarning
        )

    # 温度范围检查
    if (T < 20) or (T > 300):
        warnings.warn(
            "Extrapolating model equation for Si beyond temperature range of 20 K – 300 K",
            RuntimeWarning
        )

    S1 = np.polyval([3.4469e-12, -5.823e-09, 4.2169e-06, -0.00020802, 10.491], T)
    S2 = np.polyval([-1.3509e-06, 0.0010594, -0.27872, 29.166, -1346.6], T)
    S3 = np.polyval([103.24, 678.41, -76158, -1.7621e6, 4.4283e7], T)

    x1 = np.polyval([2.3248e-14, -2.5105e-10, 1.6713e-07, -1.1423e-05, 0.29971], T)
    x2 = np.polyval([-1.1321e-06, 0.001175, -0.35796, 42.389, -3517.1], T)
    x3 = np.polyval([23.577, -39.37, -6907.4, -1.4498e5, 1.714e6], T)

    # ===== Sellmeier 公式 =====
    n = np.sqrt(
        1
        + S1 * x**2 / (x**2 - x1**2)
        + S2 * x**2 / (x**2 - x2**2)
        + S3 * x**2 / (x**2 - x3**2)
    )

    return n
