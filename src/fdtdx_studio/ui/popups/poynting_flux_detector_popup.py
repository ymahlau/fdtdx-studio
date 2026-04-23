from nicegui import ui

from fdtdx_studio.ui.popups.base_detector_popup import BaseDetectorPopup


class PoyntingFluxDetectorPopup(BaseDetectorPopup):
    DETECTOR_TYPE = "POYNTING"

    def __init__(self, controller):
        self.input_direction = None
        self.input_axis = None
        self.input_keep_all = None
        super().__init__(controller)

    def build_detector_specific_ui(self):
        ui.label("Poynting Flux Parameters").style("font-size: 14px; font-weight: bold; margin-bottom: 6px")

        self.input_direction = ui.select(options=["+", "-"], value="+", label="Direction").classes("w-full")

        self.input_axis = ui.select(
            options={0: "X-Axis", 1: "Y-Axis", 2: "Z-Axis"}, value=0, label="Propagation Axis"
        ).classes("w-full")

        self.input_keep_all = ui.checkbox("Keep All Components", value=False)

    def collect_detector_kwargs(self) -> dict:
        assert self.input_direction is not None
        assert self.input_axis is not None
        assert self.input_keep_all is not None
        return {
            "direction": self.input_direction.value,
            "fixed_propagation_axis": self.input_axis.value,
            "keep_all_components": self.input_keep_all.value,
        }

    def close_self(self):
        super().close_self()
