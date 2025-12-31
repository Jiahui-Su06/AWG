import numpy as np
from numpy import cos, sin, pi, rad2deg, atan
import gdsfactory as gf
from gdsfactory.typings import LayerSpec


def bend_s_ring(
    w: float = 0.5,
    h: float = 10.0,
    width: float = 0.5,
    x_center: float = 0.0,
    y_center: float = 0.0,
    angle_resolution: float = 2.5,
    radius_min: float = 10,
    layer: LayerSpec = (1, 0)
) -> gf.Component:
    """绘制由两个圆环拼接而成的 S bend
            |<------ w ------>|
                       _______ _
                      /        ^
                     /         |
                    /          h
                   /           |
      start ______/           _v_

    Args:
        w: S bend 的宽度
        h: S bend 的高度，可以是负数，符号代表方向
        width: Bend 的波导宽度
        x_center: S bend 的起始点坐标 x
        y_center: S bend 的起始点坐标 y
        angle_resolution: resolution of the ring.
        radius_min: 构成Bend的圆环所允许的最小半径
        layer: gdsfactory layer
    """

    if h >= 0:
        direction = 1
    else:
        h = -h
        direction = 0

    if w <= 0:
        raise ValueError(f"width={w} must be > 0")

    c = gf.Component()
    theta = 2 * atan(h / width)
    radius = width / sin(theta) / 2
    if radius < radius_min:
        raise ValueError(f"radius={h} must be >= {radius_min}")
    inner_radius = radius - w / 2
    outer_radius = radius + w / 2
    angle = rad2deg(theta)
    n = int(np.round(angle / angle_resolution)) + 1
    if direction == 1:
        x_ring1 = x_center
        y_ring1 = y_center + radius
        x_ring2 = x_ring1 + radius * 2 * sin(theta)
        y_ring2 = y_ring1 - radius * 2 * cos(theta)
        t1 = np.linspace(-90, -90 + angle, n) * pi / 180
        t2 = np.linspace(90, 90 + angle, n) * pi / 180
    else:
        x_ring1 = x_center
        y_ring1 = y_center - radius
        x_ring2 = x_ring1 + radius * 2 * sin(theta)
        y_ring2 = y_ring1 + radius * 2 * cos(theta)
        t1 = np.linspace(90-angle, 90, n) * pi / 180
        t2 = np.linspace(-90-angle, -90, n) * pi / 180

    inner_points_x_1 = x_ring1 + inner_radius * cos(t1)
    inner_points_y_1 = y_ring1 + inner_radius * sin(t1)
    outer_points_x_1 = x_ring1 + outer_radius * cos(t1)
    outer_points_y_1 = y_ring1 + outer_radius * sin(t1)
    inner_points_x_2 = x_ring2 + inner_radius * cos(t2)
    inner_points_y_2 = y_ring2 + inner_radius * sin(t2)
    outer_points_x_2 = x_ring2 + outer_radius * cos(t2)
    outer_points_y_2 = y_ring2 + outer_radius * sin(t2)
    if direction == 1:
        x = np.concatenate([inner_points_x_1, outer_points_x_2[::-1], inner_points_x_2, outer_points_x_1[::-1]])
        y = np.concatenate([inner_points_y_1, outer_points_y_2[::-1], inner_points_y_2, outer_points_y_1[::-1]])
    else:
        x = np.concatenate([inner_points_x_1[::-1], outer_points_x_2, inner_points_x_2[::-1], outer_points_x_1])
        y = np.concatenate([inner_points_y_1[::-1], outer_points_y_2, inner_points_y_2[::-1], outer_points_y_1])
    c.add_polygon(points=list(zip(x, y, strict=False)), layer=layer)
    return c
