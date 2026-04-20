from nicegui import ui
from fdtdx_studio.ui.popups.base_detector_popup import BaseDetectorPopup

class ModeOverlapDetectorPopup(BaseDetectorPopup):
    """
    UI popup for creating an fdtdx.ModeOverlapDetector.
    """
    DETECTOR_TYPE = 'MODE_OVERLAP'

    def __init__(self, controller):
        self.input_direction = None
        self.input_axis = None
        self.input_filter_pol = None
        self.input_mode_index = None
        self.wave_button = None
        self.wave = 'Frequency'
        self.wave_value = None
        self.input_wave_char = None
        super().__init__(controller)

    def build_detector_specific_ui(self):
        ui.label('Mode Overlap Parameters') \
            .style('font-size: 14px; font-weight: bold; margin-bottom: 6px')

        # Direction: Singular, matching 'direction' in fdtdx class
        self.input_direction = ui.select(
            options=['+', '-'],
            value='+',
            label='Direction'
        ).classes('w-full')

        self.input_axis = ui.select(
            options={0: 'X-Axis', 1: 'Y-Axis', 2: 'Z-Axis'},
            value=0,
            label='Propagation Axis'
        ).classes('w-full')

        ui.label('Wave Character').style('font-size: 14px; font-weight: bold; margin-top: 8px; margin-bottom: 8px')
        with ui.dropdown_button('Frequency').classes('w-full') as self.wave_button:
          ui.item('Wavelength', on_click=lambda: self.set_wave('Wavelength'))
          ui.item('Period', on_click=lambda: self.set_wave('Period'))
          ui.item('Frequency', on_click=lambda: self.set_wave('Frequency'))
          self.wave_value = ui.number('Frequency Value', value=1.0)
          self.input_phase_shift = ui.number('Phase Shift', value=0.0)

        # Filter Polarization: Updated to 'te'/'tm' matching your error trace
        self.input_filter_pol = ui.select(
            options=['te', 'tm'],
            value=None,
            label='Filter Polarization',
            clearable=True
        ).classes('w-full')

        self.input_mode_index = ui.number(
            label='Mode Index',
            value=0,
            min=0,
            precision=0
        ).classes('w-full')

    def collect_detector_kwargs(self) -> dict:
        assert self.input_direction is not None
        assert self.input_axis is not None
        assert self.input_filter_pol is not None
        assert self.input_mode_index is not None
        return {
            'direction': self.input_direction.value,
            'fixed_propagation_axis': self.input_axis.value,
            # Wrap single selection in a tuple because signature demands Sequence[WaveCharacter]
            'wave_characters': (self.wave,),
            'filter_pol': self.input_filter_pol.value,
            'mode_index': int(self.input_mode_index.value),
        }

    def close_self(self):
        super().close_self()
        
    #These are very ugly and can probably be polished into one at some point
    def set_wave(self, wave):
        """Sets the Wave Type and updates the button display."""
        assert self.wave_value is not None
        self.wave_value.label = f'{wave} Value'
        assert self.wave_button is not None
        self.wave_button.close()
        self.wave = wave
        self.wave_button.text = f'{wave}'