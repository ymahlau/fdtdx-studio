from nicegui import ui

from fdtdx_studio.ui.popups.base_detector_popup import BaseDetectorPopup


class PhasorDetectorPopup(BaseDetectorPopup):
    """
    UI popup for creating an fdtdx.PhasorDetector.
    """

    DETECTOR_TYPE = "PHASOR"

    def __init__(self, controller):
        self.input_direction = None
        self.input_axis = None
        self.input_components = None
        self.input_filter_pol = None
        self.input_wave_char = None
        super().__init__(controller)

    def build_detector_specific_ui(self):
        ui.label("Phasor Parameters").style("font-size: 14px; font-weight: bold; margin-bottom: 6px")

        self.input_direction = ui.select(options=["+", "-"], value=None, label="Direction", clearable=True).classes(
            "w-full"
        )

        self.input_axis = ui.select(
            options={0: "X-Axis", 1: "Y-Axis", 2: "Z-Axis"}, value=None, label="Propagation Axis", clearable=True
        ).classes("w-full")

        self.input_wave_char = ui.select(
            options=["standing", "forward", "backward"], value="standing", label="Wave Character"
        ).classes("w-full")

        self.input_components = ui.select(
            options=["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"], multiple=True, value=["Ex", "Ey", "Ez"], label="Components"
        ).classes("w-full")

        self.input_filter_pol = ui.select(
            options=["te", "tm"], value=None, label="Filter Polarization", clearable=True
        ).classes("w-full")

    def collect_detector_kwargs(self) -> dict:
        assert self.input_direction is not None
        assert self.input_axis is not None
        assert self.input_wave_char is not None
        assert self.input_components is not None
        assert self.input_filter_pol is not None
        return {
            "direction": self.input_direction.value,
            "fixed_propagation_axis": self.input_axis.value,
            # Wrap in tuple for Sequence[WaveCharacter]
            "wave_characters": (self.input_wave_char.value,),
            "components": tuple(self.input_components.value) if self.input_components.value else None,
            "filter_pol": self.input_filter_pol.value,
        }

    def close_self(self):
        super().close_self()
        assert self.input_direction is not None
        assert self.input_axis is not None
        assert self.input_wave_char is not None
        assert self.input_components is not None
        assert self.input_filter_pol is not None
        self.input_direction.value = None
        self.input_axis.value = None
        self.input_wave_char.value = "standing"
        self.input_components.value = ["Ex", "Ey", "Ez"]
        self.input_filter_pol.value = None
