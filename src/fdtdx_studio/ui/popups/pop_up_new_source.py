from typing import Any, cast

from nicegui import ui
from fdtdx_studio.ui.popups.new_pop_up import new_pop_up as NewPopUp, add_tooltip_icon, labeled_number, _tip


class pop_up_new_source(NewPopUp):
  """Popup for creating a new simulation source."""

  def __init__(self, controller):
    super().__init__(controller)
    # choose which source variant to add (UNIFORM or GAUSSIAN)
    self.source_kind = 'MODE'
    # button will call wrapper which dispatches to controller method based on selection
    self.button_function = lambda: self._call_add()
    self.button_label = 'Add Source'
    self.direction_button = None
    self.kind_button = None
    self.filter_pol_button = None
    self.wave_button = None
    self.popup_new_source = None

    self.temp_profile_value1 = None  # phase_shift or center_frequency
    self.temp_profile_value2 = None  # num_startup_periods or spectral_width
    self.temporal_profile_type = 'SingleFrequencyProfile'  # Default type
    self.temp_profile_button = None

    # Source Attributes
    self.input_direction = '-'
    self.wave = 'Wavelength'
    self.wave_value = None
    self.input_phase_shift = None
    self.azimuth_angle = None
    self.elevation_angle = None
    self.temporal_profile = 'Single Frequency'
    # OnOffSwitch fields
    self.switch_start_time = None
    self.switch_start_after_periods = None
    self.switch_end_time = None
    self.switch_end_after_periods = None
    self.switch_on_for_time = None
    self.switch_on_for_periods = None
    self.switch_period = None
    self.switch_interval = None
    self.switch_fixed_on_time_steps = None
    self.switch_is_always_off = None
    # Mode Source Attributes
    self.filter_pol = 'te'
    self.mode_index = None
    # Gaussian Source Attributes
    self.radius = None
    self.normalize_by_energy: bool = True
    self.fixed_E_y = None
    self.fixed_E_x = None
    self.fixed_E_z = None
    self.fixed_H_x = None
    self.fixed_H_y = None
    self.fixed_H_z = None
    self.std = None

    self.build_dialog()

  def _call_add(self):
    """Dispatch add call to controller based on selected source kind."""
    if self.source_kind == 'MODE':
        assert self.mode_index is not None
    else:
        assert self.radius and self.std
        assert self.fixed_E_x and self.fixed_E_y and self.fixed_E_z
        assert self.fixed_H_x and self.fixed_H_y and self.fixed_H_z

    assert self.input_name and self.input_length and self.input_width and self.input_height
    assert self.wave_value and self.input_phase_shift and self.azimuth_angle and self.elevation_angle
    assert self.temp_profile_value1 and self.temp_profile_value2
    assert self.switch_start_time and self.switch_start_after_periods
    assert self.switch_end_time and self.switch_end_after_periods
    assert self.switch_on_for_time and self.switch_on_for_periods
    assert self.switch_period and self.switch_interval
    assert self.popup_new_source

    kwargs = dict(
      popup=self.popup_new_source,
      typ='scrollarea_sim_sources',
      name=self.input_name.value,
      partial_real_shape=(self.input_length.value, self.input_width.value, self.input_height.value),
      color=self.input_color,
      direction=self.input_direction,
      wave=dict(
        frequency=self.wave_value.value if self.wave == 'Frequency' else None,
        period=self.wave_value.value if self.wave == 'Period' else None,
        wavelength=self.wave_value.value if self.wave == 'Wavelength' else None,
        phase_shift=self.input_phase_shift.value,
      ),
      azimuth_angle=self.azimuth_angle.value,
      elevation_angle=self.elevation_angle.value,
      switch=dict(
        start_time=self.switch_start_time.value,
        start_after_periods=self.switch_start_after_periods.value,
        end_time=self.switch_end_time.value,
        end_after_periods=self.switch_end_after_periods.value,
        on_for_time=self.switch_on_for_time.value,
        on_for_periods=self.switch_on_for_periods.value,
        period=self.switch_period.value,
        interval=self.switch_interval.value,
        fixed_on_time_steps=(
            None if not self.switch_fixed_on_time_steps or not self.switch_fixed_on_time_steps.value
            else [int(s.strip()) for s in str(self.switch_fixed_on_time_steps.value).split(',') if s.strip()]
        ),
        is_always_off=self.switch_is_always_off,
      ),
      filter_pol=None if self.source_kind == 'GAUSSIAN' else self.filter_pol,
      mode_index=None if self.source_kind == 'GAUSSIAN' else self.mode_index.value,
      radius=None if self.source_kind == 'MODE' else self.radius.value,
      std=None if self.source_kind == 'MODE' else self.std.value,
      normalize_by_energy=None if self.source_kind == 'MODE' else self.normalize_by_energy,
      fixed_E_polarization_vector=None if self.source_kind == 'MODE' else [self.fixed_E_x.value, self.fixed_E_y.value, self.fixed_E_z.value],
      fixed_H_polarization_vector=None if self.source_kind == 'MODE' else [self.fixed_H_x.value, self.fixed_H_y.value, self.fixed_H_z.value],
    )
    if self.temporal_profile_type == 'SingleFrequencyProfile':
      kwargs['temporal_profile'] = dict(
        type='SingleFrequencyProfile',
        phase_shift=self.temp_profile_value1.value,
        num_startup_periods=self.temp_profile_value2.value,
      )
    elif self.temporal_profile_type == 'GaussianPulseProfile':
      kwargs['temporal_profile'] = dict(
        type='GaussianPulseProfile',
        center_frequency=self.temp_profile_value1.value,
        spectral_width=self.temp_profile_value2.value,
      )
    if self.source_kind == 'GAUSSIAN':
      kwargs.pop('filter_pol')
      kwargs.pop('mode_index')
      self.controller.add_gaussian_source(**kwargs)
    else:
      kwargs.pop('normalize_by_energy')
      kwargs.pop('fixed_E_polarization_vector')
      kwargs.pop('fixed_H_polarization_vector')
      kwargs.pop('radius')
      kwargs.pop('std')
      self.controller.add_mode_source(**kwargs)
    self.popup_new_source.close()
    return

  def build_dialog(self):
    """Builds the dialog UI for the popup. (Overrides superclass method)"""
    with ui.dialog() as self.popup_new_source, ui.card():
      # Type selector at very top
      with ui.dropdown_button(f'Type: {self.source_kind}').classes('w-full') as self.kind_button:
        ui.item('MODE', on_click=lambda: self.set_kind('MODE'))
        ui.item('GAUSSIAN', on_click=lambda: self.set_kind('GAUSSIAN'))

      with ui.row():
        with ui.column():
          self.build_common_ui()
          assert self.input_name and self.input_width and self.input_length and self.input_height
          self.input_name.set_value("New Source")
          self.input_width.set_value(10e-6)
          self.input_length.set_value(10e-6)
          self.input_height.set_value(0)
          with ui.row():
            with ui.dropdown_button('Direction: -').classes('w-full') as self.direction_button:
              ui.item('+', on_click=lambda: self.set_direction('+'))
              ui.item('-', on_click=lambda: self.set_direction('-'))

          # Temporal Profile
          ui.label('Temporal Profile').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
          self.temporal_profile_button = ui.select(
              ['SingleFrequencyProfile', 'GaussianPulseProfile'],
              on_change=lambda: self.set_temp_profile_type(),
              label='Profile Type',
              value='SingleFrequencyProfile',
          )

          self._temp_profile_container = ui.column().classes('w-full gap-1')
          self._build_temp_profile_fields()

          ui.label('Angles').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
          with ui.row().classes('w-full items-center gap-1'):
            self.elevation_angle = ui.number('Elevation angle', value=0.0)
            add_tooltip_icon(_tip('elevation_angle'))
          with ui.row().classes('w-full items-center gap-1'):
            self.azimuth_angle = ui.number('Azimuth angle', value=0.0)
            add_tooltip_icon(_tip('azimuth_angle'))

          ui.label('Wave Character').style('font-size: 14px; font-weight: bold; margin-top: 8px; margin-bottom: 8px')
          with ui.dropdown_button('Wavelength').classes('w-full') as self.wave_button:
            ui.item('Wavelength', on_click=lambda: self.set_wave('Wavelength'))
            ui.item('Period', on_click=lambda: self.set_wave('Period'))
            ui.item('Frequency', on_click=lambda: self.set_wave('Frequency'))
          with ui.row().classes('w-full items-center gap-1'):
            self.wave_value = ui.number('Wavelength Value', value=1.550e-6)
            add_tooltip_icon(_tip('wavelength'))
          with ui.row().classes('w-full items-center gap-1'):
            self.input_phase_shift = ui.number('Phase Shift', value=0.0)
            add_tooltip_icon(_tip('phase_shift'))

        # OnOffSwitch parameters column
        with ui.column():
          ui.label('OnOffSwitch') \
            .style('font-size: 14px; font-weight: bold; margin-top: 8px; margin-bottom: 8px')

          with ui.row().classes('w-full items-center gap-1'):
            self.switch_start_time = ui.number('Start Time', value=None)
            add_tooltip_icon(_tip('start_time'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_start_after_periods = ui.number('Start After Periods', value=None)
            add_tooltip_icon(_tip('start_after_periods'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_end_time = ui.number('End Time', value=None)
            add_tooltip_icon(_tip('end_time'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_end_after_periods = ui.number('End After Periods', value=None)
            add_tooltip_icon(_tip('end_after_periods'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_on_for_time = ui.number('On For Time', value=None)
            add_tooltip_icon(_tip('on_for_time'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_on_for_periods = ui.number('On For Periods', value=None)
            add_tooltip_icon(_tip('on_for_periods'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_period = ui.number('Switch Period', value=None)
            add_tooltip_icon(_tip('period'))
          with ui.row().classes('w-full items-center gap-1'):
            self.switch_interval = ui.number('Interval', value=1, min=1, step=1)
            add_tooltip_icon(_tip('interval'))
          self.switch_fixed_on_time_steps = ui.input('Fixed On Time Steps', placeholder='e.g., 100,250,500')
          ui.checkbox('Switch Is Always Off', on_change=lambda s: setattr(self, 'switch_is_always_off', s.value))

        cast(Any, self.make_source_mode_options)()

      self.add_button(self.button_function, self.button_label)

  def _build_temp_profile_fields(self):
    """(Re)build the temporal profile value fields with matching tooltips."""
    self._temp_profile_container.clear()
    with self._temp_profile_container:
      if self.temporal_profile_type == 'GaussianPulseProfile':
        lbl1, key1 = 'Center Frequency', 'center_frequency'
        lbl2, key2 = 'Spectral Width', 'spectral_width'
      else:
        lbl1, key1 = 'Phase Shift', 'phase_shift'
        lbl2, key2 = 'Num of Startup Periods', 'num_startup_periods'
      with ui.row().classes('w-full items-center gap-1'):
        self.temp_profile_value1 = ui.number(lbl1).classes('flex-1').props('dense')
        add_tooltip_icon(_tip(key1))
      with ui.row().classes('w-full items-center gap-1'):
        self.temp_profile_value2 = ui.number(lbl2).classes('flex-1').props('dense')
        add_tooltip_icon(_tip(key2))

  def set_temp_profile_type(self, temporal_profile_type=None):
    """Sets the temporal profile type and rebuilds the value fields with correct tooltips."""
    if temporal_profile_type:
      self.temporal_profile_type = temporal_profile_type
      self.temporal_profile_button.value = temporal_profile_type
    else:
      self.temporal_profile_type = self.temporal_profile_button.value
    self._build_temp_profile_fields()

  @ui.refreshable
  def make_source_mode_options(self):
    """Makes a refreshable part of the Dialog that changes based on which Source Type is selected"""
    if self.source_kind == 'MODE':
      with ui.row().classes('w-full items-center gap-1'):
        self.mode_index = ui.number('Mode Index', value=0, min=0, step=1)
        add_tooltip_icon(_tip('mode_index'))
      with ui.dropdown_button(f'Filter pol: {self.filter_pol}').classes('w-full') as self.filter_pol_button:
        ui.item('te', on_click=lambda: self.set_filter('te'))
        ui.item('tm', on_click=lambda: self.set_filter('tm'))
    else:  # GAUSSIAN
      with ui.column():
        ui.label("General").style('font-size: 14px; font-weight: bold; margin-top: 8px; margin-bottom: 8px')
        with ui.row().classes('w-full items-center gap-1'):
          self.radius = ui.number('Radius', value=4e-6, min=0.0, step=1e-6)
          add_tooltip_icon(_tip('radius'))
        with ui.row().classes('w-full items-center gap-1'):
          self.std = ui.number('Standard Deviation', value=(1/3), min=0.0, step=0.1)
          add_tooltip_icon(_tip('std'))
      ui.checkbox('Normalize by Energy', value=self.normalize_by_energy, on_change=lambda s: setattr(self, 'normalize_by_energy', s.value))
      with ui.column():
        ui.label('Fixed E Polarization Vector').style('font-size: 14px; font-weight: bold; margin-top: 8px; margin-bottom: 8px')
        self.fixed_E_x = ui.number('x', value=1)
        self.fixed_E_y = ui.number('y', value=0)
        self.fixed_E_z = ui.number('z', value=0)
      with ui.column():
        ui.label('Fixed H Polarization Vector').style('font-size: 14px; font-weight: bold; margin-top: 8px; margin-bottom: 8px')
        self.fixed_H_x = ui.number('x', value=None)
        self.fixed_H_y = ui.number('y', value=None)
        self.fixed_H_z = ui.number('z', value=None)

  def open_new_source_popup(self):
    assert self.popup_new_source
    self.popup_new_source.open()

  def set_wave(self, wave):
    """Sets the Wave Type and updates the button display."""
    assert self.wave_value
    assert self.wave_button
    self.wave_value.label = f'{wave} Value'
    self.wave_button.close()
    self.wave = wave
    self.wave_button.text = f'{wave}'

  def set_direction(self, direction):
    """Sets the direction and updates the button display."""
    assert self.direction_button
    self.direction_button.close()
    self.input_direction = direction
    self.direction_button.text = f'Direction: {direction}'

  def set_filter(self, filter):
    """Sets the filter_pol and updates the button display."""
    assert self.filter_pol_button
    self.filter_pol_button.close()
    self.filter_pol = filter
    self.filter_pol_button.text = f'Filter pol: {filter}'

  def set_kind(self, kind: str):
    """Set source kind (MODE or GAUSSIAN) and update UI label."""
    self.source_kind = kind
    if self.kind_button:
      self.kind_button.close()
      self.kind_button.text = f'Type: {kind}'
    self.make_source_mode_options.refresh()
