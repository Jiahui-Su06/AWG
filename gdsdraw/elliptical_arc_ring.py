import numpy as np
import gdsfactory as gf


def ellipse_arc_points(
    a: float = 10.0,
    b: float = 5.0,
    theta_start: float = 0.0,
    theta_stop: float = 360.0,
    rotate_angle: float = 0.0,
    angle_resolution: float = 1.0,
    center: tuple[float, float] = (0.0, 0.0),
) -> np.ndarray:
    """生成椭圆弧坐标点

    Parameters
    ----------
    a (float): 椭圆长半轴
    b (float): 椭圆短半轴
    theta_start (float): 椭圆弧线起始角度（单位：度）
    theta_stop (float): 终止角度
    rotate_angle (float): 椭圆旋转角度（相对于椭圆中心）
    angle_resolution (float): 绘图角分辨率（度）
    center (tuple[float, float]): 椭圆中心点坐标

    Returns
    -------
    np.ndarray: 椭圆弧离散点坐标

    """
    # 输入检测：a长半轴  和短半轴 b 大于 0
    if a <= 0:
        raise ValueError(f"a={a} must be > 0")
    elif b <= 0:
        raise ValueError(f"b={b} must be > 0")

    # 根据角分辨率计算绘图所用坐标点总数
    num_points = int(np.round(np.abs(theta_stop-theta_start) / angle_resolution)) + 1
    # 防止超出 theta_stop 的范围
    theta = np.linspace(np.deg2rad(theta_start), np.deg2rad(theta_stop), num_points)

    # 计算椭圆坐标，计算大量数据采用 numpy 库
    x = a * np.cos(theta)
    y = b * np.sin(theta)

    # 旋转椭圆，利用旋转矩阵实现
    rotate_angle_rad = np.deg2rad(rotate_angle)
    xr = x * np.cos(rotate_angle_rad) - y * np.sin(rotate_angle_rad)
    yr = x * np.sin(rotate_angle_rad) + y * np.cos(rotate_angle_rad)

    # 平移椭圆
    x_final = xr + center[0]
    y_final = yr + center[1]

    return np.column_stack((x_final, y_final))


def elliptical_arc_ring(
    a_inner: float = 0.0,
    b_inner: float = 0.0,
    a_outer: float = 0.0,
    b_outer: float = 0.0,
    theta_start: float = 0.0,
    theta_stop: float = 0.0,
    rotate_angle: float = 0.0,
    angle_resolution: float = 1.0,
    center: tuple[float, float] = (0.0, 0.0),
    layer: tuple[int, int] = (1, 0)
) -> gf.Component:
    """绘制椭圆弧环
    参数：
        a_inner, b_inner (float): 内椭圆 a 和 b 长度
        a_outer, b_outer (float): 外椭圆 a 和 b 长度
        theta_start, theta_stop: 椭圆坐标系中的起止角度 (度)
        rotate_angle: 椭圆环整体旋转角度 (度)
        angle_resolution (float): 绘图角分辨率
        center (float): 椭圆环中心
        layer (float): 绘制层
    """
    c = gf.Component()

    # 外弧 (正向)
    outer_arc = ellipse_arc_points(a_outer, b_outer, theta_start, theta_stop, rotate_angle=rotate_angle,
                                   angle_resolution=angle_resolution, center=center)
    # 内弧 (反向)
    inner_arc = ellipse_arc_points(a_inner, b_inner, theta_stop, theta_start, rotate_angle=rotate_angle,
                                   angle_resolution=angle_resolution, center=center)

    # 拼接椭圆环
    ring_points = np.vstack([outer_arc, inner_arc])
    c.add_polygon(ring_points, layer=layer)

    return c
