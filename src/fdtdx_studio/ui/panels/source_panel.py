from nicegui import ui

from fdtdx_studio.ui.panels.object_config_panel import ObjectConfigPanel
from fdtdx_studio.ui.panels.switch_element import SwitchElement


class SourcePanel(ObjectConfigPanel):
    """Parent Class of all specific Sources. Generates UI for general source parameters."""

    def __init__(self, view, controller):
        """
        Initializes the SourcePanel with references to the main view and controller.

        :param view: reference to the main UI view
        :param controller: reference to the main controller
        :type view: View
        :type controller: Controller
        """

        # Initialize Controller and widgets as in superclass
        super().__init__(view, controller)
        # general source widgets

        # azimuth_angle widget (Standard Value: float -> 0.0)
        self.azimuth_angle = None

        # direction widget (Literal ['+', ['-']])
        self.direction = None

        # elevation_angle widget (Standard Value: float -> 0.0)
        self.elevation_angle = None

        # max_angle_random_offset widget (Standard Value: float -> 0.0)
        self.max_angle_random_offset = None

        # max_horizontal_offset (Standard Value: float -> 0.0)
        self.max_horizontal_offset = None

        # static_amplitude_factor (Standard Value: float -> 1.0)
        self.static_amplitude_factor = None

        # temporal_profile (SingleFrequencyProfile(phase_shift=#3.141592653589793, num_startup_periods=4))

        self.temp_profile_value1 = None  # phase_shift or center_frequency
        self.temp_profile_value2 = None  # num_startup_periods or spectral_width
        self.temporal_profile_type = "SingleFrequencyProfile"  # Default type
        self.temp_profile_button = None

        # Todo: Wiederverwendbares Element Switch bauen
        # Switch (switch=OnOffSwitch(   start_time=#None, start_after_periods=#None, end_time=#None, end_after_periods=#None, on_for_time=#None, on_for_periods=#None, period=#None, fixed_on_time_steps=#None, is_always_off=#False, interval=#1 ))
        self.switch = None

        # Todo: Wave Character Widget seperat machen?
        # Wave Character Widgets and Helper (Object of class WaveCharakter, default: None)
        self.wave_phase_shift = None
        self.wave_period = None
        self.wave_length = None
        self.wave_frequency = None
        self.wave_button = None
        self.wave_value = None
        self.wave = "Frequency"  # Default wave type

    def render_into(self, panel):
        """
        Render general source parameters and use render_source_type_parameters to render subclasses.
        param panel: The UI panel to render the source parameters into.
        type panel: nicegui.ui.column
        """

        super().render_into(panel)

        with panel:
            # Direction and Angle Parameters
            ui.label("Direction & Angles").style(
                "font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;"
            ).tooltip("Sets the direction and angles of the source.")
            with ui.column().style("padding-left: 4px").classes("w-full"):
                # Note: UI elements no longer call `update_button_state` on change (deprecated).
                self.direction = ui.select(["+", "-"], label="Direction", value="+").classes("w-3/4")
                self.azimuth_angle = (
                    ui.number("Azimuth Angle", validation=self._validate_float).classes("flex-1").props("dense")
                )
                self.elevation_angle = (
                    ui.number("Elevation Angle", validation=self._validate_float).classes("flex-1").props("dense")
                )
                self.max_angle_random_offset = (
                    ui.number("Max Angel Random Offset", validation=self._validate_float)
                    .classes("flex-1")
                    .props("dense")
                )

            # Horizontal Offset
            ui.label("Horizontal Offset").style(
                "font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;"
            ).tooltip("Maximum horizontal offset of the source.")
            with ui.column().classes("w-full"):
                self.max_horizontal_offset = (
                    ui.number("Max Offset", validation=self._validate_float).classes("flex-1").props("dense")
                )

            # Amplitude
            ui.label("Static Amplitude Factor").style(
                "font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;"
            ).tooltip("Static amplitude factor for the source.")
            with ui.column().style("padding-left: 8px").classes("w-full"):
                self.static_amplitude_factor = (
                    ui.number("Factor", validation=self._validate_float).classes("flex-1").props("dense")
                )

            # Temporal Profile
            ui.label("Temporal Profile").style(
                "font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;"
            ).tooltip("Temporal profile settings (phase shift and startup periods).")
            self.temporal_profile_button = ui.select(
                ["SingleFrequencyProfile", "GaussianPulseProfile"],
                on_change=lambda: self.set_temp_profile_type(),
                label="Profile Type",
                value="SingleFrequencyProfile",
            ).classes("w-3/4")
            with ui.column().style("padding-left: 6px").classes("w-full") as self.temp_profile_display:
                self.temp_profile_value1 = (
                    ui.number("Phase Shift", validation=self._validate_float).classes("flex-1").props("dense")
                )
                self.temp_profile_value2 = (
                    ui.number("Num of Startup Periods", validation=self._validate_float)
                    .classes("flex-1")
                    .props("dense")
                )

            # Wave Character
            ui.label("Wave Character").style(
                "font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;"
            ).tooltip("Wave character parameters.")
            with ui.dropdown_button("Frequency").classes("w-full") as self.wave_button:
                ui.item("Wavelength", on_click=lambda: self.set_wave("Wavelength"))
                ui.item("Period", on_click=lambda: self.set_wave("Period"))
                ui.item("Frequency", on_click=lambda: self.set_wave("Frequency"))
            self.wave_value = ui.number("Frequency Value", value=1.0)
            self.wave_phase_shift = ui.number("Phase Shift", value=0.0)

            # Switch Element
            self.switch = SwitchElement(self, controller=self.controller)
            self.switch.build_on_off_switch_panel()

    def set_temp_profile_type(self, temporal_profile_type=None):
        """
        Sets the temporal profile type and changes the labels of the values accordingly.
        param temporal_profile_type: The type of temporal profile to set. Either None, SingleFrequencyProfile or GaussianPulseProfile. If None, uses the current selection from the UI.
        type temporal_profile_type: str | None
        """
        if temporal_profile_type:
            self.temporal_profile_type = temporal_profile_type
            self.temporal_profile_button.value = temporal_profile_type
        else:
            self.temporal_profile_type = self.temporal_profile_button.value

        if self.temporal_profile_type == "SingleFrequencyProfile":
            if self.temp_profile_value1:
                self.temp_profile_value1.label = "Phase Shift"
            if self.temp_profile_value2:
                self.temp_profile_value2.label = "Num of Startup Periods"
        elif self.temporal_profile_type == "GaussianPulseProfile":
            if self.temp_profile_value1:
                self.temp_profile_value1.label = "Center Frequency"
            if self.temp_profile_value2:
                self.temp_profile_value2.label = "Spectral Width"

    def set_wave(self, wave):
        """
        Sets the Wave Type and updates the button display.
        param wave: The type of wave character to set. Either 'Wavelength', 'Period', or 'Frequency'.
        type wave: str
        """
        if self.wave_value:
            self.wave_value.label = f"{wave} Value"
        if self.wave_button:
            self.wave_button.close()
            self.wave_button.text = f"{wave}"
        self.wave = wave

    def get_parameters(self):
        """
        Add specific parameters for subclasses to implement.
        :return: Dictionary of current parameter values.
        :rtype: dict
        """
        parameters = super().get_parameters()
        parameters["direction"] = self.direction.value if self.direction else None
        parameters["azimuth_angle"] = self.azimuth_angle.value if self.azimuth_angle else None
        parameters["elevation_angle"] = self.elevation_angle.value if self.elevation_angle else None
        parameters["max_angle_random_offset"] = (
            self.max_angle_random_offset.value if self.max_angle_random_offset else None
        )
        parameters["max_horizontal_offset"] = self.max_horizontal_offset.value if self.max_horizontal_offset else None
        parameters["static_amplitude_factor"] = (
            self.static_amplitude_factor.value if self.static_amplitude_factor else None
        )
        # Temporal Profile parameters
        parameters["temporal_profile"] = {
            "type": self.temporal_profile_type,
        }
        if self.temporal_profile_type == "SingleFrequencyProfile":
            parameters["temporal_profile"]["phase_shift"] = (
                self.temp_profile_value1.value if self.temp_profile_value1 else None
            )
            parameters["temporal_profile"]["num_startup_periods"] = (
                self.temp_profile_value2.value if self.temp_profile_value2 else None
            )
        elif self.temporal_profile_type == "GaussianPulseProfile":
            parameters["temporal_profile"]["center_frequency"] = (
                self.temp_profile_value1.value if self.temp_profile_value1 else None
            )
            parameters["temporal_profile"]["spectral_width"] = (
                self.temp_profile_value2.value if self.temp_profile_value2 else None
            )
        else:
            raise ValueError(f"Unknown temporal profile type: {self.temporal_profile_type}")
        # Switch parameters
        if self.switch:
            parameters["switch"] = self.switch.get_parameters()
        # Wave Character parameters
        if self.wave_phase_shift:
            parameters["wave_character"] = {
                "phase_shift": self.wave_phase_shift.value,
            }
        match self.wave:
            case "Frequency":
                if self.wave_value:
                    parameters["wave_character"]["frequency"] = self.wave_value.value
            case "Period":
                if self.wave_value:
                    parameters["wave_character"]["period"] = self.wave_value.value
            case "Wavelength":
                if self.wave_value:
                    parameters["wave_character"]["wavelength"] = self.wave_value.value

        return parameters

    def update_values(self, parameters):
        """
        Updates the Source UI elements with the provided parameters.
        :param parameters: Dictionary containing parameters of the source to be configured
        :type parameters: dict
        """

        # update general object parameters
        super().update_values(parameters)

        # sets all general source values of widgets from parameters dict
        if "direction" in parameters:
            self.set_direction(parameters["direction"])
        if "azimuth_angle" in parameters:
            self.set_azimuth_angle(parameters["azimuth_angle"])
        if "elevation_angle" in parameters:
            self.set_elevation_angle(parameters["elevation_angle"])
        if "max_angle_random_offset" in parameters:
            self.set_max_angle_random_offset(parameters["max_angle_random_offset"])
        if "max_horizontal_offset" in parameters:
            self.set_max_horizontal_offset(parameters["max_horizontal_offset"])
        if "static_amplitude_factor" in parameters:
            self.set_static_amplitude_factor(parameters["static_amplitude_factor"])
        if "temporal_profile" in parameters:
            temp_profile = parameters["temporal_profile"]
            self.set_temp_profile_type(type(temp_profile).__name__)
            if type(temp_profile).__name__ == "SingleFrequencyProfile":
                self.set_phase_shift(temp_profile.phase_shift)
                self.set_num_startup_periods(temp_profile.num_startup_periods)
            elif type(temp_profile).__name__ == "GaussianPulseProfile":
                self.set_center_frequency(temp_profile.center_frequency)
                self.set_spectral_width(temp_profile.spectral_width)
        if "wave_character" in parameters:
            wave_char = parameters["wave_character"]
            if wave_char.phase_shift is not None:
                self.set_wave_phase_shift(wave_char.phase_shift)
            if wave_char.period is not None:
                self.set_wave("Period")
                if self.wave_value:
                    self.wave_value.value = wave_char.period
            elif wave_char.wavelength is not None:
                self.set_wave("Wavelength")
                if self.wave_value:
                    self.wave_value.value = wave_char.wavelength
            elif wave_char.frequency is not None:
                self.set_wave("Frequency")
                if self.wave_value:
                    self.wave_value.value = wave_char.frequency

        if self.switch and "switch" in parameters:
            self.switch.update_values(parameters["switch"])

    def _validate_float(self, value) -> str | None:
        """Validation function to check if input is a float or empty."""
        try:
            float(value)
            if value is None or value == "":
                return None
        except (ValueError, TypeError):
            if value is not None:
                return "Input must be a float number like 0.0"
            return None

    def on_save_clicked(self):
        """
        Save button click handler for SourcePanel.
        Calls the superclass method to handle general saving behavior.
        """
        super().on_save_clicked()

    # General Source Setters

    def set_direction(self, direction):
        """Update direction dropdown."""
        if self.direction:
            self.direction.value = direction

    def set_azimuth_angle(self, angle):
        """Update azimuth angle."""
        if self.azimuth_angle:
            self.azimuth_angle.value = angle

    def set_elevation_angle(self, angle):
        """Update elevation angle."""
        if self.elevation_angle:
            self.elevation_angle.value = angle

    def set_max_angle_random_offset(self, offset):
        """Update max angle random offset."""
        if self.max_angle_random_offset:
            self.max_angle_random_offset.value = offset

    def set_max_horizontal_offset(self, offset):
        """Update max horizontal offset."""
        if self.max_horizontal_offset:
            self.max_horizontal_offset.value = offset

    def set_static_amplitude_factor(self, factor):
        """Update static amplitude factor."""
        if self.static_amplitude_factor:
            self.static_amplitude_factor.value = factor

    # Temporal Profile Setters
    def set_phase_shift(self, phase_shift):
        """Update phase shift."""
        if self.temp_profile_value1:
            self.temp_profile_value1.value = phase_shift

    def set_num_startup_periods(self, periods):
        """Update number of startup periods."""
        if self.temp_profile_value2:
            self.temp_profile_value2.value = periods

    def set_center_frequency(self, frequency):
        """Update center frequency."""
        if self.temp_profile_value1 and self.temporal_profile_type == "GaussianPulseProfile":
            self.temp_profile_value1.value = frequency

    def set_spectral_width(self, width):
        """Update spectral width."""
        if self.temp_profile_value2 and self.temporal_profile_type == "GaussianPulseProfile":
            self.temp_profile_value2.value = width

    # Wave Character Setters

    def set_wave_phase_shift(self, shift):
        """Update wave phase shift."""
        if self.wave_phase_shift:
            self.wave_phase_shift.value = shift

    def set_wave_period(self, period):
        """Update wave period."""
        if self.wave_period:
            self.wave_period.value = period

    def set_wave_length(self, length):
        """Update wave length."""
        if self.wave_length:
            self.wave_length.value = length

    def set_wave_frequency(self, frequency):
        """Update wave frequency."""
        if self.wave_frequency:
            self.wave_frequency.value = frequency
