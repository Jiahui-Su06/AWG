import numpy as np


def Air(x):
    """
    Refractive index of Air (idealized n=1)

    Parameters
    ----------
    x : float or array_like
        Wavelength(s) in micrometers (µm)

    Returns
    -------
    n : float or ndarray
        Refractive index (always 1)
    """
    x = np.asarray(x)  # 确保向量化
    n = np.ones_like(x, dtype=float)

    # 如果输入是标量，返回标量
    if n.size == 1:
        return n.item()
    return n
