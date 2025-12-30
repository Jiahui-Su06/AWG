import numpy as np
from numpy import cos, sin, pi
import gdsfactory as gf
from gdsfactory.typings import LayerSpec


def ring_arc(
    radius: float = 10.0,
    width: float = 0.5,
    theta_start: float = 0.0,
    theta_stop: float = 90.0,
    x_center: float = 0.0,
    y_center: float = 0.0,
    angle_resolution: float = 2.5,
    layer: LayerSpec = (1, 0)
) -> gf.Component:
    """Returns a ring arc.

    Args:
        radius: radius of the ring.
        width: width of the ring.
        theta_start: starting angle of the ring.
        theta_stop: stopping angle of the ring.
        x_center: 圆环弧的中心坐标x
        y_center: 圆环弧的中心坐标y
        angle_resolution: resolution of the ring.
        layer: gdsfactory layer
    """
    if radius <= 0:
        raise ValueError(f"radius={radius} must be > 0")
    if width <= 0:
        raise ValueError(f"width={width} must be > 0")
    if theta_stop < theta_start:
        raise ValueError(f"theta_stop={theta_stop} must be >= theta_start={theta_start}")

    c = gf.Component()
    inner_radius = radius - width / 2
    outer_radius = radius + width / 2
    n = int(np.round((theta_stop - theta_start) / angle_resolution)) + 1
    t = np.linspace(theta_start, theta_stop, n) * pi / 180
    inner_points_x = x_center + inner_radius * cos(t)
    inner_points_y = y_center + inner_radius * sin(t)
    outer_points_x = x_center + outer_radius * cos(t)
    outer_points_y = y_center + outer_radius * sin(t)
    x = np.concatenate([inner_points_x, outer_points_x[::-1]])
    y = np.concatenate([inner_points_y, outer_points_y[::-1]])
    c.add_polygon(points=list(zip(x, y, strict=False)), layer=layer)
    return c
