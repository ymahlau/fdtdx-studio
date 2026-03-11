from dataclasses import dataclass
from typing import Optional, Dict, List, Any

@dataclass
class AttributeDef:
    name: str
    label: str
    ui_type: str # 'number', 'string', 'boolean', 'select', 'color', 'nested', 'vector3'
    importance: int # > 0 means visible by default
    default: Any = None
    options: Optional[List[Any]] = None # For 'select' type
    tooltip: Optional[str] = None
    target_cls: Optional[str] = None # For 'nested' type, the class of the nested object

# Metadata definitions for fdtdx objects
OBJECT_DEFINITIONS: Dict[str, List[AttributeDef]] = {
    'GaussianPlaneSource': [
        AttributeDef('name', 'Name', 'string', 10, tooltip='Unique name of the source'),
        AttributeDef('direction', 'Direction', 'select', 10, options=['+', '-'], default='+', tooltip='Direction of propagation'),
        AttributeDef('azimuth_angle', 'Azimuth Angle', 'number', 9, default=0.0, tooltip='Azimuth angle in degrees'),
        AttributeDef('elevation_angle', 'Elevation Angle', 'number', 9, default=0.0, tooltip='Elevation angle in degrees'),
        AttributeDef('static_amplitude_factor', 'Amplitude Factor', 'number', 8, default=1.0, tooltip='Static amplitude scaling factor'),
        AttributeDef('color', 'Color', 'color', 8, default='#FF0000', tooltip='Display color in the 3D scene'),
        AttributeDef('temporal_profile', 'Temporal Profile', 'nested', 7, target_cls='TemporalProfile'),
        AttributeDef('switch', 'Switch', 'nested', 6, target_cls='OnOffSwitch'),
        AttributeDef('wave_character', 'Wave Character', 'nested', 6, target_cls='WaveCharacter'),
        
        # New attributes
        AttributeDef('fixed_E_polarization_vector', 'Fixed E Polarization', 'vector3', 5, default=(0.0, 0.0, 0.0), tooltip='Fixed Electric field polarization vector'),
        AttributeDef('fixed_H_polarization_vector', 'Fixed H Polarization', 'vector3', 5, default=(0.0, 0.0, 0.0), tooltip='Fixed Magnetic field polarization vector'),
        AttributeDef('normalize_by_energy', 'Normalize by Energy', 'boolean', 5, default=True, tooltip='Normalize source power by energy'),
        AttributeDef('radius', 'Radius', 'number', 5, default=0.0, tooltip='Radius of the Gaussian beam'),
        AttributeDef('std', 'Standard Deviation', 'number', 5, default=0.33, tooltip='Standard deviation of the Gaussian profile'),

        AttributeDef('max_angle_random_offset', 'Max Angle Random Offset', 'number', 0, default=0.0),
        AttributeDef('max_horizontal_offset', 'Max Horizontal Offset', 'number', 0, default=0.0),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
    ],
    'ModePlaneSource': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('direction', 'Direction', 'select', 10, options=['+', '-'], default='+'),
        AttributeDef('mode_index', 'Mode Index', 'number', 10, default=0),
        AttributeDef('filter_pol', 'Filter Polarization', 'select', 9, options=['te', 'tm', None], default=None, tooltip="Polarization filter"),
        AttributeDef('temporal_profile', 'Temporal Profile', 'nested', 8, target_cls='TemporalProfile'),
        AttributeDef('switch', 'Switch', 'nested', 6, target_cls='OnOffSwitch'),
        AttributeDef('wave_character', 'Wave Character', 'nested', 6, target_cls='WaveCharacter'),
        AttributeDef('color', 'Color', 'color', 8, default='#0000FF'),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
    ],
    'UniformMaterialObject': [
         AttributeDef('name', 'Name', 'string', 10),
         AttributeDef('material', 'Material', 'material_select', 10),
         AttributeDef('color', 'Color', 'color', 10, default='#808080'),
         AttributeDef('partial_real_position', 'Position', 'vector3', 10, default=(0.0, 0.0, 0.0)),
         AttributeDef('partial_real_shape', 'Size', 'vector3', 10, default=(1.0, 1.0, 1.0)),
    ],
    'FieldDetector': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('plot', 'Plot', 'boolean', 9, default=False),
        AttributeDef('reduce_volume', 'Reduce Volume', 'boolean', 8, default=False),
        AttributeDef('plot_dpi', 'Plot DPI', 'number', 7, default=100),
        AttributeDef('components', 'Components', 'multi_select', 9, options=['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'], default=['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']),
        AttributeDef('num_time_steps_recorded', 'Num Time Steps Recorded', 'number', 5),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
        AttributeDef('color', 'Color', 'color', 5, default='#00FF00'),
        AttributeDef('switch', 'Switch', 'nested', 4, target_cls='OnOffSwitch'),
        # Shared detector attributes
        AttributeDef('dtype', 'Data Type', 'select', 8, options=['float32', 'float64'], default='float32'),
        AttributeDef('exact_interpolation', 'Exact Interpolation', 'boolean', 0, default=False),
        AttributeDef('inverse', 'Inverse', 'boolean', 0, default=False),
        AttributeDef('if_inverse_plot_backwards', 'Inverse Plot Backwards', 'boolean', 0, default=False),
        AttributeDef('num_video_workers', 'Num Video Workers', 'number', 0, default=0),
        AttributeDef('plot_interpolation', 'Plot Interpolation', 'string', 0, default='gaussian'),
    ],
    'EnergyDetector': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('plot_dpi', 'Plot DPI', 'number', 8, default=100),
        AttributeDef('as_slices', 'As Slices', 'boolean', 9, default=False),
        AttributeDef('x_slice', 'X Slice', 'number', 7, default=0.0),
        AttributeDef('y_slice', 'Y Slice', 'number', 7, default=0.0),
        AttributeDef('z_slice', 'Z Slice', 'number', 7, default=0.0),
        AttributeDef('reduce_volume', 'Reduce Volume', 'boolean', 5, default=False),
        AttributeDef('color', 'Color', 'color', 5, default='#FFFF00'),
        AttributeDef('switch', 'Switch', 'nested', 4, target_cls='OnOffSwitch'),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef('dtype', 'Data Type', 'select', 8, options=['float32', 'float64'], default='float32'),
        AttributeDef('exact_interpolation', 'Exact Interpolation', 'boolean', 0, default=False),
        AttributeDef('inverse', 'Inverse', 'boolean', 0, default=False),
        AttributeDef('if_inverse_plot_backwards', 'Inverse Plot Backwards', 'boolean', 0, default=False),
        AttributeDef('num_video_workers', 'Num Video Workers', 'number', 0, default=0),
        AttributeDef('plot_interpolation', 'Plot Interpolation', 'string', 0, default='gaussian'),
    ],
    'PoyntingFluxDetector': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('direction', 'Direction', 'select', 9, options=['+', '-'], default='+'),
        AttributeDef('fixed_propagation_axis', 'Fixed Prop Axis', 'number', 9, default=0),
        AttributeDef('keep_all_components', 'Keep All Components', 'boolean', 8, default=False),
        AttributeDef('plot_dpi', 'Plot DPI', 'number', 7, default=100),
        AttributeDef('switch', 'Switch', 'nested', 4, target_cls='OnOffSwitch'),
        AttributeDef('color', 'Color', 'color', 5, default='#FFA500'),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef('dtype', 'Data Type', 'select', 8, options=['float32', 'float64'], default='float32'),
        AttributeDef('exact_interpolation', 'Exact Interpolation', 'boolean', 0, default=False),
        AttributeDef('inverse', 'Inverse', 'boolean', 0, default=False),
        AttributeDef('if_inverse_plot_backwards', 'Inverse Plot Backwards', 'boolean', 0, default=False),
        AttributeDef('num_video_workers', 'Num Video Workers', 'number', 0, default=0),
        AttributeDef('plot_interpolation', 'Plot Interpolation', 'string', 0, default='gaussian'),
    ],
    'PhasorDetector': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('direction', 'Direction', 'select', 9, options=['+', '-'], default=None),
        AttributeDef('fixed_propagation_axis', 'Fixed Prop Axis', 'number', 9, default=None),
        AttributeDef('components', 'Components', 'multi_select', 9, options=['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'], default=[]),
        AttributeDef('filter_pol', 'Filter Pol', 'select', 8, options=['h', 'v', None], default=None),
        AttributeDef('wave_character', 'Wave Character', 'select', 8, options=['standing', 'forward', 'backward'], default='standing'),
        AttributeDef('plot_dpi', 'Plot DPI', 'number', 7, default=100),
        AttributeDef('switch', 'Switch', 'nested', 4, target_cls='OnOffSwitch'),
        AttributeDef('color', 'Color', 'color', 5, default='#00FFFF'),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef('dtype', 'Data Type', 'select', 8, options=['float32', 'float64'], default='float32'),
        AttributeDef('exact_interpolation', 'Exact Interpolation', 'boolean', 0, default=False),
        AttributeDef('inverse', 'Inverse', 'boolean', 0, default=False),
        AttributeDef('if_inverse_plot_backwards', 'Inverse Plot Backwards', 'boolean', 0, default=False),
        AttributeDef('num_video_workers', 'Num Video Workers', 'number', 0, default=0),
        AttributeDef('plot_interpolation', 'Plot Interpolation', 'string', 0, default='gaussian'),
    ],
    'ModeOverlapDetector': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('direction', 'Direction', 'select', 9, options=['+', '-'], default='+'),
        AttributeDef('mode_index', 'Mode Index', 'number', 9, default=0),
        AttributeDef('filter_pol', 'Filter Pol', 'select', 8, options=['te', 'tm', None], default=None),
        AttributeDef('plot_dpi', 'Plot DPI', 'number', 7, default=100),
        AttributeDef('switch', 'Switch', 'nested', 4, target_cls='OnOffSwitch'),
         AttributeDef('color', 'Color', 'color', 5, default='#FF00FF'),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef('dtype', 'Data Type', 'select', 8, options=['float32', 'float64'], default='float32'),
        AttributeDef('exact_interpolation', 'Exact Interpolation', 'boolean', 0, default=False),
        AttributeDef('inverse', 'Inverse', 'boolean', 0, default=False),
        AttributeDef('if_inverse_plot_backwards', 'Inverse Plot Backwards', 'boolean', 0, default=False),
        AttributeDef('num_video_workers', 'Num Video Workers', 'number', 0, default=0),
        AttributeDef('plot_interpolation', 'Plot Interpolation', 'string', 0, default='gaussian'),
    ],
    'OnOffSwitch': [
        AttributeDef('start_time', 'Start Time', 'number', 5),
        AttributeDef('start_after_periods', 'Start After Periods', 'number', 5),
        AttributeDef('end_time', 'End Time', 'number', 5),
        AttributeDef('end_after_periods', 'End After Periods', 'number', 5),
        AttributeDef('on_for_time', 'On For Time', 'number', 5),
        AttributeDef('on_for_periods', 'On For Periods', 'number', 5),
        AttributeDef('period', 'Period', 'number', 5),
        AttributeDef('interval', 'Interval', 'number', 5, default=1),
        AttributeDef('is_always_off', 'Always Off', 'boolean', 5, default=False),
    ],
    'SingleFrequencyProfile': [
        AttributeDef('phase_shift', 'Phase Shift', 'number', 10, default=0.0),
        AttributeDef('num_startup_periods', 'Num Startup Periods', 'number', 10, default=0),
    ],
    'GaussianPulseProfile': [
        AttributeDef('center_frequency', 'Center Frequency', 'number', 10),
        AttributeDef('spectral_width', 'Spectral Width', 'number', 10),
        AttributeDef('phase_shift', 'Phase Shift', 'number', 10),
    ],
    'WaveCharacter': [
        AttributeDef('phase_shift', 'Phase Shift', 'number', 10, default=0.0),
        AttributeDef('wavelength', 'Wavelength', 'number', 5),
        AttributeDef('frequency', 'Frequency', 'number', 5),
        AttributeDef('period', 'Period', 'number', 5),
    ]
}
