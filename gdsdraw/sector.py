import numpy as np
from numpy import cos, sin
import gdsfactory as gf
from gdsfactory.typings import LayerSpec


def sector(
    radius: float = 10.0,
    angle_start: float = 0.0,
    angle_stop: float = 90.0,
    x_center: float = 0.0,
    y_center: float = 0.0,
    angle_resolution: float = 2.5,
    layer: LayerSpec = (1, 0)
) -> gf.Component:
    """Generate a circle geometry.

    Args:
        radius: of the circle.
        angle_start: starting angle of the sector.
        angle_stop: stopping angle of the sector.
        x_center: 扇形的中心坐标x
        y_center: 扇形的中心坐标y
        angle_resolution: number of degrees per point.
        layer: layer.
    """
    if radius <= 0:
        raise ValueError(f"radius={radius} must be > 0")
    if angle_stop <= angle_start:
        raise ValueError(f"theta_stop={angle_stop} must be > theta_start={angle_start}")
    c = gf.Component()
    num_points = int(np.round((angle_stop - angle_start) / angle_resolution)) + 1
    theta = np.deg2rad(np.linspace(angle_start, angle_stop, num_points, endpoint=True))
    points = np.stack((x_center + radius * cos(theta), y_center + radius * sin(theta)), axis=-1)
    points = np.append(points, np.array([[x_center, y_center]]), axis=0)
    c.add_polygon(points=points, layer=layer)
    return c
