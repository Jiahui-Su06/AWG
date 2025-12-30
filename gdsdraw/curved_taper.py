import numpy as np
import gdsfactory as gf


def curved_taper(
    m: float = 2.0,
    w1: float = 1.0,
    w2: float = 2.0,
    length: float = 10.0,
    n: int = 100,
    rotate_angle: float = 0.0,
    center: tuple[float, float] = (0.0, 0.0),
    layer: tuple[int, int] = (1, 0)
) -> gf.Component:
    """绘制锥形波导
        参数：
            m (float): m参数
            w1, w2 (float): taper短边、长边宽度
            length (float): taper长度
            n (int): 描点数目
            rotate_angle (float): 锥形波导倾斜角度（度）
            center (float): 锥形波导短边中心
            layer (float): gdsfactory绘制层
        """

    c = gf.Component()
    alpha = (w1 - w2) / (length ** m)
    x = np.linspace(0, length, n)
    w = alpha * (length - x) ** m + w2
    y1 = w / 2
    y2 = - w / 2
    p1 = np.column_stack((x, y1))  # 锥形上段点
    p2 = np.column_stack((x, y2))  # 下段
    vtx = []
    vtx.extend(p1)
    vtx.extend(p2[::-1])
    theta = np.deg2rad(180)  # 旋转角度（°→弧度）
    rotate = np.array([[np.cos(theta), -np.sin(theta)],
                       [np.sin(theta), np.cos(theta)]])  # 旋转矩阵
    # 旋转
    vtx_rot = vtx @ rotate.T
    # 平移
    offset = np.array([length, 0])  # 平移目标点 (x0, y0)
    vtx_new = vtx_rot + offset
    theta = np.deg2rad(rotate_angle)  # 旋转角度（°→弧度）
    rotate = np.array([[np.cos(theta), -np.sin(theta)],
                       [np.sin(theta), np.cos(theta)]])  # 旋转矩阵
    # 旋转
    vtx_rot = vtx_new @ rotate.T
    # 平移
    offset = np.array(center)  # 平移目标点 (x0, y0)
    vtx_new = vtx_rot + offset
    c.add_polygon(vtx_new, layer=layer)
    return c
