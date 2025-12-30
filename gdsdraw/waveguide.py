import numpy as np
import gdsfactory as gf


def waveguide(
    start: tuple[float, float] = (0.0, 0.0),
    end: tuple[float, float] = (10.0, 0.0),
    width: float = 0.5,
    layer: tuple[int, int] = (1, 0)
) -> gf.Component:
    """已知起点、终点，绘制直波导

    参数：
        start (tuple[float, float]): 波导起始点
        end (tuple[float, float]): 直波导终止点
        width (float): 波导宽度
        layer (tuple[int, int]): 绘制层
    """
    dx, dy = end[0]-start[0], end[1]-start[1]
    length = np.sqrt(dx**2 + dy**2)
    angle = np.degrees(np.arctan2(dy, dx))

    xs = gf.cross_section.strip(width=width, layer=layer)
    wg = gf.components.straight(length=length, cross_section=xs)

    c = gf.Component()
    ref = c.add_ref(wg)
    ref.move(start)
    ref.rotate(angle, center=start)
    return c
