from nicegui import ui


class SwitchElement:
    # === OnOffSwitch Configuration ===
    def __init__(self, surrounding_panel, controller, paramaters=None):
        """
        Initializes the SwitchElement with a reference to the surrounding panel.
        Changes will effect the validity of the button in the surrounding panel.

        :param surrounding_panel: Reference to the parent panel (must have on_save_clicked() methods)
        """
        self.switch_container = None
        self.surrounding_panel = surrounding_panel

        self.controller = controller

    def build_on_off_switch_panel(self):
        """Builds the OnOffSwitch configuration panel."""
        ui.label("OnOffSwitch Configuration").style(
            "font-size: 14px; font-weight: bold; margin-top: 24px; margin-bottom: 8px"
        ).tooltip("Precise temporal control over when the detector is active")

        self.start_time = (
            ui.number(label="Start Time", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Absolute simulation time when detector turns on")
        )

        self.start_after_periods = (
            ui.number(label="Start After Periods", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Turn on after this many source periods have elapsed")
        )

        self.end_time = (
            ui.number(label="End Time", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Absolute simulation time when detector turns off")
        )

        self.end_after_periods = (
            ui.number(label="End After Periods", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Turn off after this many source periods from start")
        )

        self.on_for_time = (
            ui.number(label="On For Time", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Duration (in time units) the detector stays on once activated")
        )

        self.on_for_periods = (
            ui.number(label="On For Periods", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Duration (in source periods) the detector stays on")
        )

        self.period = (
            ui.number(label="Period", format="%.6f", value=None)
            .props("clearable")
            .classes("w-full")
            .tooltip("Period length used for period-based timing controls")
        )

        self.interval = (
            ui.number(label="Interval", value=1, min=1, step=1)
            .classes("w-full")
            .tooltip("Recording/update interval in time steps")
        )

        self.fixed_on_time_steps = (
            ui.input(label="Fixed On Time Steps", placeholder="e.g., 100, 250, 500")
            .classes("w-full")
            .tooltip("Force detector ON at these exact time steps (comma-separated)")
        )

        self.is_always_off = ui.checkbox("Is Always Off").tooltip(
            "Completely disable the detector regardless of other settings"
        )

    def get_parameters(self):
        """
        Gathers the current OnOffSwitch configuration parameters.
        :return:
            dict: Dictionary containing the current switch parameters.
        """
        parameters = {
            "start_time": self.start_time.value,
            "start_after_periods": self.start_after_periods.value,
            "end_time": self.end_time.value,
            "end_after_periods": self.end_after_periods.value,
            "on_for_time": self.on_for_time.value,
            "on_for_periods": self.on_for_periods.value,
            "period": self.period.value,
            "interval": self.interval.value,
            "fixed_on_time_steps": self.fixed_on_time_steps.value,
            "is_always_off": self.is_always_off.value,
        }
        return parameters

    def update_values(self, parameters):
        """
        Update the panel's UI elements with the provided parameters.
        :param parameters: FDTDX SwitchOnOff Object containing the switch parameters to set.
        """

        self.start_time.value = parameters.start_time
        self.start_after_periods.value = parameters.start_after_periods
        self.end_time.value = parameters.end_time
        self.end_after_periods.value = parameters.end_after_periods
        self.on_for_time.value = parameters.on_for_time
        self.on_for_periods.value = parameters.on_for_periods
        self.period.value = parameters.period
        self.interval.value = parameters.interval
        self.fixed_on_time_steps.value = parameters.fixed_on_time_steps
        self.is_always_off.value = parameters.is_always_off
