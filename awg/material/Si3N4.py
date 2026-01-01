import numpy as np
import warnings


def Si3N4(x):
    """
    Refractive index of Si3N4 using Sellmeier model

    Material model (Sellmeier) for: Si3N4 @ 20 °C
    Valid wavelength range: 0.31 µm – 5.504 µm
    Source: https://refractiveindex.info/?shelf=main&book=Si3N4&page=Luke

    Parameters
    ----------
    x : float or array_like
        Wavelength in micrometers (µm)

    Returns
    -------
    n : float or ndarray
        Refractive index of Si3N4
    """

    # 转为 numpy 数组
    x = np.asarray(x, dtype=float)

    # 波长范围检查
    if np.any(x < 0.31) or np.any(x > 5.504):
        warnings.warn(
            "Extrapolating Sellmeier equation for Si3N4 beyond range 0.31–5.504 µm",
            RuntimeWarning
        )

    # Sellmeier 方程
    n = np.sqrt(
        1
        + 3.0249 / (1 - (0.1353406 / x) ** 2)
        + 40314 / (1 - (1239.842 / x) ** 2)
    )

    return n
