import math

from nicegui import ui


class CoordinateSystem(ui.scene.group):
    def __init__(self, name: str, *, length: float = 1.0) -> None:
        super().__init__()

        with self:
            for label, color, rx, ry, rz in [
                ("x", "#ff0000", 0, 0, -math.pi / 2),
                ("y", "#00ff00", 0, 0, 0),
                ("z", "#0000ff", math.pi / 2, 0, 0),
            ]:
                with ui.scene.group().rotate(rx, ry, rz):
                    ui.scene.cylinder(0.02 * length, 0.02 * length, 0.8 * length).move(y=0.4 * length).material(color)
                    ui.scene.cylinder(0, 0.1 * length, 0.2 * length).move(y=0.9 * length).material(color)
                    ui.scene.text(label, style=f"color: {color}").move(y=1.1 * length)
            ui.scene.text(name, style="color: #808080")
