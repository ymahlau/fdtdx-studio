from nicegui import ui

from fdtdx_studio.ui.popups.base_detector_popup import BaseDetectorPopup


class FieldDetectorPopup(BaseDetectorPopup):
    """
    UI popup for creating an fdtdx.FieldDetector.

    Responsibilities:
    - define detector-specific UI fields
    - collect detector-specific parameters
    - provide DETECTOR_TYPE for controller dispatch

    IMPORTANT:
    - does NOT own a dialog
    - does NOT talk to the controller directly
    """

    # Used by BaseDetectorPopup._call_add()
    # >>> CONTROLLER DISPATCH KEY <<<
    DETECTOR_TYPE = "FIELD"

    def __init__(self, controller):
        # >>> UI ONLY <<<
        # Initialize detector-specific input references

        self.input_average = None
        self.input_normalize = None

        # Initialize BaseDetectorPopup (stores controller, sets button)
        super().__init__(controller)

    # --------------------------------------------------
    # DETECTOR-SPECIFIC UI
    # --------------------------------------------------

    def build_detector_specific_ui(self):
        """
        Build UI elements specific to FieldDetector.

        This method is called from BaseDetectorPopup.build_dialog_inside().
        """
        # >>> UI ONLY <<<

        ui.label("Field Components").style("font-size: 14px; font-weight: bold; margin-bottom: 6px")

        ALL_COMPONENTS = ["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"]

        # 👉 EINZIGE QUELLE DER WAHRHEIT
        self.component_enabled = {c: True for c in ALL_COMPONENTS}

        self._component_buttons = {}

        def sync_button(c):
            btn = self._component_buttons[c]
            if self.component_enabled[c]:
                # 🔵 aktiv = blau
                btn.props(remove="outline")
                btn.props("unelevated color=primary")
            else:
                # ⚪ inaktiv = weiß
                btn.props(remove="unelevated color=primary")
                btn.props("outline")

        with ui.row().classes("gap-2"):
            for comp in ALL_COMPONENTS:

                def on_click(c=comp):
                    self.component_enabled[c] = not self.component_enabled[c]
                    sync_button(c)

                btn = ui.button(comp, on_click=lambda e, c=comp: on_click(c))
                self._component_buttons[comp] = btn
                sync_button(comp)

        # Optional detector behavior flags
        self.input_average = ui.checkbox("Spatial Average", value=False)
        self.input_normalize = ui.checkbox("Normalize", value=False)

    # --------------------------------------------------
    # DATA COLLECTION (UI → Controller)
    # --------------------------------------------------

    def collect_detector_kwargs(self) -> dict:
        """
        Collect parameters specific to FieldDetector.

        Returned dict is merged into the controller call in
        BaseDetectorPopup._call_add().
        """
        # >>> UI ONLY <<<
        assert self.input_average is not None
        assert self.input_normalize is not None
        return {
            "components": tuple(c for c, enabled in self.component_enabled.items() if enabled),
            "average": self.input_average.value,
            "normalize": self.input_normalize.value,
        }

    # --------------------------------------------------
    # RESET (NO dialog handling!)
    # --------------------------------------------------

    def close_self(self):
        """
        Reset detector-specific UI state.

        Called by:
        - DetectorPopup when switching detector types
        - Controller after successful detector creation
        """
        # >>> UI ONLY <<<
        super().close_self()

        for c in self.component_enabled:
            self.component_enabled[c] = True

            btn = self._component_buttons.get(c)
            if btn:
                # ALLES Relevante zurücksetzen
                btn.props(remove="outline unelevated color=primary")
                # explizit wieder blau setzen
                btn.props("unelevated color=primary")

        assert self.input_average is not None
        assert self.input_normalize is not None
        self.input_average.value = False
        self.input_normalize.value = False
