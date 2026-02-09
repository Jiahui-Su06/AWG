import numpy as np

def overlap(x, u, v, hu=None, hv=None):
    """
    Overlap integral (1D)

    DESCRIPTION:
        Computes the overlap integral in 1D with or without H field.

    INPUTS:
        x  - coordinate vector
        u  - incident electric field
        v  - outgoing electric field
        hu - (optional) incident magnetic field
        hv - (optional) outgoing magnetic field

    OUTPUT:
        t  - power coupling efficiency
    """

    # 转为 numpy 数组并拉直
    x = np.asarray(x)
    u = np.asarray(u).reshape(-1)
    v = np.asarray(v).reshape(-1)

    # ---------- E + H 场重叠 ----------
    if hu is not None and hv is not None:
        hu = np.asarray(hu).reshape(-1)
        hv = np.asarray(hv).reshape(-1)

        uu = np.trapz(u * np.conj(hu), x)
        vv = np.trapz(v * np.conj(hv), x)
        uv = np.trapz(u * np.conj(hv), x)
        vu = np.trapz(v * np.conj(hu), x)

        t = np.abs(np.real(uv * vu / vv) / np.real(uu))

    # ---------- 仅 E 场重叠 ----------
    else:
        uu = np.trapz(np.conj(u) * u, x)
        vv = np.trapz(np.conj(v) * v, x)
        uv = np.trapz(np.conj(u) * v, x)

        t = np.abs(uv) / (np.sqrt(uu) * np.sqrt(vv))
        # 等价另一种写法：
        # t = np.abs(uv)**2 / (uu * vv)

    return t
