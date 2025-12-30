import gdsfactory as gf
from gdsfactory.typings import LayerSpec


def mmi1x2(
    width: float = 1.0,
    width_taper: float = 2.0,
    length_taper_in: float = 10.0,
    length_taper_out: float = 20.0,
    length_mmi: float = 30.0,
    width_mmi: float = 10.0,
    gap_mmi: float = 2.0,
    cross_section="strip",
    layer: LayerSpec | None = None,
):

    c = gf.Component()

    # ======================
    # 输入 taper
    # ======================
    taper_in = gf.components.taper(
        length=length_taper_in,
        width1=width,
        width2=width_taper,
        cross_section=cross_section,
        layer=layer
    )
    t_in = c.add_ref(taper_in)
    t_in.move((0, 0))  # y=0 保证对齐

    # ======================
    # MMI 区（矩形）
    # ======================
    mmi = gf.components.rectangle(
        size=(length_mmi, width_mmi),
        layer=layer,
    )
    m = c.add_ref(mmi)
    # 对齐左边界到输入 taper 的右边
    m.xmin = t_in.xmax
    # 保证 y 中心对齐
    m.y = 0

    # ======================
    # 输出 tapers
    # ======================
    taper_out = gf.components.taper(
        length=length_taper_out,
        width1=width_taper,
        width2=width,
        cross_section=cross_section,
        layer=layer
    )

    y_offset = gap_mmi / 2 + width_taper / 2

    t_out1 = c.add_ref(taper_out)
    t_out2 = c.add_ref(taper_out)

    # 对齐输入端到 MMI 右边
    t_out1.xmin = m.xmax
    t_out2.xmin = m.xmax
    # 对齐 y
    t_out1.y = +y_offset
    t_out2.y = -y_offset

    # ======================
    # 端口定义
    # ======================
    c.add_port("o1", port=t_in.ports["o1"], cross_section=cross_section, layer=layer)
    c.add_port("o2", port=t_out1.ports["o2"], cross_section=cross_section, layer=layer)
    c.add_port("o3", port=t_out2.ports["o2"], cross_section=cross_section, layer=layer)

    return c
