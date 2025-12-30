import gdsfactory as gf
from numpy import cos, sin, deg2rad


def taper(
    w1: float = 1.0,
    w2: float = 2.0,
    length: float = 10.0,
    rotate_angle: float = 0.0,
    center: tuple[float, float] = (0.0, 0.0),
    layer: tuple[int, int] = (1, 0)
) -> gf.Component:
    """绘制锥形波导
        参数：
            w1, w2 (float): taper短边、长边宽度
            length (float): taper长度
            rotate_angle (float): 锥形波导倾斜角度（度）
            center (float): 锥形波导短边中心
            layer (float): gdsfactory绘制层
        """

    c = gf.Component()
    x = center[0]
    y = center[1]
    theta = deg2rad(rotate_angle)
    v1 = [x + w1 / 2 * sin(theta), y - w1 / 2 * cos(theta)]
    v2 = [x - w1 / 2 * sin(theta), y + w1 / 2 * cos(theta)]
    v3 = [x + length * cos(theta) - w2 / 2 * sin(theta),
          y + length * sin(theta) + w2 / 2 * cos(theta)]
    v4 = [x + length * cos(theta) + w2 / 2 * sin(theta),
          y + length * sin(theta) - w2 / 2 * cos(theta)]
    vtx = [v1,
           v2,
           v3,
           v4]
    c.add_polygon(vtx, layer=layer)
    return c
