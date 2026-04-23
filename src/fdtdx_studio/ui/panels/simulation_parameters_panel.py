import re

from nicegui import ui

from fdtdx_studio.parameter.dtype import DType
from fdtdx_studio.ui.attribute_definitions import extract_all_fdtdx_docstrings
from fdtdx_studio.ui.popups.new_pop_up import add_tooltip_icon

# Static fallbacks — used when the fdtdx source has no #: docstrings for a field
_SIM_TOOLTIP_FALLBACKS = {
    "backend": "Computation backend to use for the FDTD simulation.",
    "time": "Total simulation time in seconds (supports scientific notation, e.g. 80e-15).",
    "resolution": "Spatial grid resolution in points per wavelength.",
    "courant_factor": "Courant stability factor (0 < c ≤ 1). Lower values are more stable but slower.",
    "dtype": "Floating-point precision used throughout the simulation.",
}


def _build_sim_tooltips():
    """Extract SimulationConfig docstrings dynamically, falling back to statics."""
    tips = dict(_SIM_TOOLTIP_FALLBACKS)
    try:
        all_docs = extract_all_fdtdx_docstrings()
        # Try exact class first, then any class that documents the attribute
        cls_docs = all_docs.get("SimulationConfig", {})
        for key in tips:
            if key in cls_docs:
                tips[key] = cls_docs[key]
            else:
                # Fallback: look across all classes
                for cls, docs in all_docs.items():
                    if key in docs:
                        tips[key] = docs[key]
                        break
    except Exception as e:
        print(f"Warning: Failed to extract SimulationConfig tooltips dynamically: {e}")
    return tips


_SIM_TOOLTIPS = _build_sim_tooltips()


class simulation_parameters_panel:
    def __init__(self, drawer, controller):
        self.drawer = drawer
        self.controller = controller
        self.button = None  # Initialised before validation callbacks are bound

    def simulation_param_panel(self, dialog: ui.dialog | None = None):
        ui.label("Simulation Parameters").style("font-size: 18px; margin-bottom: 8px; font-weight: bold;")

        with ui.row().classes("w-full items-center gap-1"):
            ui.select(
                ["cpu", "gpu", "tpu", "METAL"],
                label="Backend",
                value=self.controller.project.param.backend,
                on_change=lambda e: self.controller.project.param.set_backend(e.value),
            ).classes("flex-1")
            add_tooltip_icon(_SIM_TOOLTIPS["backend"])

        # Use a text input for Time so scientific notation typing isn't interrupted
        with ui.row().classes("w-full items-center gap-1"):
            time = ui.input(
                label="Time",
                value=str(self.controller.project.param.time),
                validation=self._validate_Time,
            ).classes("flex-1")
            add_tooltip_icon(_SIM_TOOLTIPS["time"])

        with ui.row().classes("w-full items-center gap-1"):
            res = ui.number(
                label="Resolution",
                value=self.controller.project.param.resolution,
                validation=self._validate,
            ).classes("flex-1")
            add_tooltip_icon(_SIM_TOOLTIPS["resolution"])

        with ui.row().classes("w-full items-center gap-1"):
            courant = ui.number(
                label="Courant Factor",
                value=self.controller.project.param.courant_factor,
                validation=self._validate,
            ).classes("flex-1")
            add_tooltip_icon(_SIM_TOOLTIPS["courant_factor"])

        with ui.row().classes("w-full items-center gap-1"):
            ui.select(
                {DType.Float_32: "Float 32", DType.Float_64: "Float 64"},
                label="Data Type",
                value=self.controller.project.param.dtype,
                on_change=lambda e: self.controller.project.param.set_dtype(e.value),
            ).classes("flex-1")
            add_tooltip_icon(_SIM_TOOLTIPS["dtype"])

        async def on_save_clicked():
            await self.saveParams(time.value, res.value, courant.value)
            await self.drawer.update_drawer()
            if dialog is not None:
                dialog.close()

        # Button is created AFTER all input widgets; validation closures reference self.button safely.
        self.button = ui.button("Apply", on_click=on_save_clicked)

    async def saveParams(self, time, res, courant):
        try:
            t = float(time)
        except (ValueError, TypeError):
            t = self.controller.project.param.time
        self.controller.project.param.set_time(t)
        self.controller.project.param.set_resolution(float(res))
        self.controller.project.param.set_courant_factor(courant)

    def _validate_Time(self, value):
        try:
            if value is None:
                self._disable_button()
                return "Input must be a number"
            s = str(value).strip()
            if s == "":
                self._disable_button()
                return "Input must be a number"
            try:
                v = float(s)
                if v > 0:
                    self._enable_button()
                    return None
                else:
                    self._disable_button()
                    return "Number must be greater than 0"
            except (ValueError, TypeError):
                partial_pattern = r"^[\s]*[+-]?(?:\d+\.?\d*|\.?\d+)(?:[eE][+-]?\d*)?[\s]*$"
                if re.match(partial_pattern, s):
                    self._disable_button()
                    return None
                else:
                    self._disable_button()
                    return "Invalid number format"
        except Exception:
            self._disable_button()
            return "Input must be a number"

    def _validate(self, value):
        try:
            if self.isFloat(value):
                self._enable_button()
                return None
            else:
                self._disable_button()
                return "Input must be a number"
        except (ValueError, TypeError):
            self._disable_button()
            return "Input must be a number"

    def _enable_button(self):
        if self.button is not None:
            self.button.enable()

    def _disable_button(self):
        if self.button is not None:
            self.button.disable()

    def isFloat(self, element: "str") -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False
