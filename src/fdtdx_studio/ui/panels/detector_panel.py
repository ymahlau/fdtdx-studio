from nicegui import ui

from fdtdx_studio.ui.panels.object_config_panel import ObjectConfigPanel
from fdtdx_studio.ui.panels.switch_element import SwitchElement


class DetectorConfigurationPanel(ObjectConfigPanel):
    """
    Configuration panel for detector-specific parameters, including advanced OnOffSwitch controls.

    This panel provides a clean, single-item-per-row interface for configuring:
    - Data type (float32/float64)
    - Boolean flags
    - Full OnOffSwitch temporal behavior
    - Video processing and plotting options
    """

    def __init__(self, view, controller):
        """
        Initialize the detector configuration panel.

        Args:
            view: Reference to the main application view
            controller: Controller handling parameter changes
        """
        super().__init__(view, controller)

        # Widget references
        self.dtype = None  #: jnp.dtype = frozen_field(default=jnp.float32)
        self.exact_interpolation = None
        self.inverse = None
        self.if_inverse_plot_backwards = None
        self.num_video_workers = None
        self.plot_interpolation = None

        # OnOffSwitch configuration widgets TODO: in poishing phase make validation() for OnOffSwitch
        self.start_time = None
        self.start_after_periods = None
        self.end_time = None
        self.end_after_periods = None
        self.on_for_time = None
        self.on_for_periods = None
        self.period = None
        self.interval = None
        self.fixed_on_time_steps = None
        self.is_always_off = None

    def render_specific_parameters(self, panel):
        """
        Render all detector-specific configuration controls.
        Each parameter appears on its own row for maximum clarity and readability.
        """
        with panel:
            # === Data Type ===
            ui.label("Data Type").style(
                "font-size: 14px; font-weight: bold; margin-top: 16px; margin-bottom: 4px"
            ).tooltip("Precision used for detector field computations")
            self.dtype = ui.select(options=["float32", "float64"], value="float32", label="Select data type").classes(
                "w-full"
            )
            # === Boolean Flags ===
            ui.label("Flags").style("font-size: 14px; font-weight: bold; margin-top: 20px; margin-bottom: 8px").tooltip(
                "Various boolean options affecting detector behavior"
            )

            self.exact_interpolation = ui.checkbox("Exact Interpolation").tooltip(
                "Use exact (slower) interpolation instead of fast approximation"
            )
            self.inverse = ui.checkbox("Inverse").tooltip("Record the inverse field (e.g., 1/E instead of E)")
            self.if_inverse_plot_backwards = ui.checkbox("If Inverse Plot Backwards").tooltip(
                "When in inverse mode, reverse the time axis in plots"
            )

            # Video & Plotting
            ui.label("Video & Plotting").style(
                "font-size: 14px; font-weight: bold; margin-top: 24px; margin-bottom: 8px"
            )

            self.num_video_workers = (
                ui.number(label="Number of Video Workers", value=0, min=0)
                .classes("w-full")
                .tooltip("Number of parallel workers for video generation (0 = auto)")
            )

            self.plot_interpolation = (
                ui.input(label="Plot Interpolation Method", value="gaussian")
                .classes("w-full")
                .tooltip("Matplotlib interpolation method used when rendering detector plots")
            )

            self.switch = SwitchElement(self, controller=self.controller)
            self.switch.build_on_off_switch_panel()

    def get_parameters(self):
        parameters = super().get_parameters()
        parameters["dtype"] = (
            self.dtype.value
            if getattr(self, "dtype", None) is not None and hasattr(self.dtype, "value")
            else (self.dtype if self.dtype is not None else None)
        )
        parameters["exact_interpolation"] = (
            self.exact_interpolation.value
            if getattr(self, "exact_interpolation", None) is not None and hasattr(self.exact_interpolation, "value")
            else (self.exact_interpolation if self.exact_interpolation is not None else None)
        )
        parameters["inverse"] = (
            self.inverse.value
            if getattr(self, "inverse", None) is not None and hasattr(self.inverse, "value")
            else (self.inverse if self.inverse is not None else None)
        )
        parameters["if_inverse_plot_backwards"] = (
            self.if_inverse_plot_backwards.value
            if getattr(self, "if_inverse_plot_backwards", None) is not None
            and hasattr(self.if_inverse_plot_backwards, "value")
            else (self.if_inverse_plot_backwards if self.if_inverse_plot_backwards is not None else None)
        )
        parameters["num_video_workers"] = (
            self.num_video_workers.value
            if getattr(self, "num_video_workers", None) is not None and hasattr(self.num_video_workers, "value")
            else (self.num_video_workers if self.num_video_workers is not None else None)
        )
        parameters["plot_interpolation"] = (
            self.plot_interpolation.value
            if getattr(self, "plot_interpolation", None) is not None and hasattr(self.plot_interpolation, "value")
            else (self.plot_interpolation if self.plot_interpolation is not None else None)
        )
        if self.switch:
            parameters["switch"] = self.switch.get_parameters()

        return parameters

    def update_values(self, parameters):

        super().update_values(parameters)
        # set values on existing UI widgets when possible, otherwise replace
        if getattr(self, "dtype", None) is not None and hasattr(self.dtype, "value"):
            self.dtype.value = parameters.get("dtype")
        else:
            self.dtype = parameters.get("dtype")

        if getattr(self, "exact_interpolation", None) is not None and hasattr(self.exact_interpolation, "value"):
            self.exact_interpolation.value = bool(parameters.get("exact_interpolation", False))
        else:
            self.exact_interpolation = parameters.get("exact_interpolation")

        if getattr(self, "inverse", None) is not None and hasattr(self.inverse, "value"):
            self.inverse.value = bool(parameters.get("inverse", False))
        else:
            self.inverse = parameters.get("inverse")

        if getattr(self, "if_inverse_plot_backwards", None) is not None and hasattr(
            self.if_inverse_plot_backwards, "value"
        ):
            self.if_inverse_plot_backwards.value = bool(parameters.get("if_inverse_plot_backwards", False))
        else:
            self.if_inverse_plot_backwards = parameters.get("if_inverse_plot_backwards")

        if getattr(self, "num_video_workers", None) is not None and hasattr(self.num_video_workers, "value"):
            self.num_video_workers.value = parameters.get("num_video_workers")
        else:
            self.num_video_workers = parameters.get("num_video_workers")

        if getattr(self, "plot_interpolation", None) is not None and hasattr(self.plot_interpolation, "value"):
            self.plot_interpolation.value = parameters.get("plot_interpolation")
        else:
            self.plot_interpolation = parameters.get("plot_interpolation")

        if self.switch and "switch" in parameters:
            self.switch.update_values(parameters["switch"])

    def on_save_clicked(self):
        super().on_save_clicked()
