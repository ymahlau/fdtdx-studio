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
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('direction', 'Direction', 'select', 10, options=['+', '-'], default='+'),
        AttributeDef('azimuth_angle', 'Azimuth Angle', 'number', 9, default=0.0),
        AttributeDef('elevation_angle', 'Elevation Angle', 'number', 9, default=0.0),
        AttributeDef('static_amplitude_factor', 'Amplitude Factor', 'number', 8, default=1.0),
        AttributeDef('color', 'Color', 'color', 8, default='#FF0000'),
        AttributeDef('temporal_profile', 'Temporal Profile', 'nested', 7, target_cls='TemporalProfile'),
        AttributeDef('switch', 'Switch', 'nested', 6, target_cls='OnOffSwitch'),
        AttributeDef('wave_character', 'Wave Character', 'nested', 6, target_cls='WaveCharacter'),
        
        # New attributes
        AttributeDef('fixed_E_polarization_vector', 'Fixed E Polarization', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('fixed_H_polarization_vector', 'Fixed H Polarization', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('normalize_by_energy', 'Normalize by Energy', 'boolean', 5, default=True),
        AttributeDef('radius', 'Radius', 'number', 5, default=0.0),
        AttributeDef('std', 'Standard Deviation', 'number', 5, default=0.33),

        AttributeDef('max_angle_random_offset', 'Max Angle Random Offset', 'number', 0, default=0.0),
        AttributeDef('max_horizontal_offset', 'Max Horizontal Offset', 'number', 0, default=0.0),
        AttributeDef('partial_real_position', 'Position', 'vector3', 5, default=(0.0, 0.0, 0.0)),
        AttributeDef('partial_real_shape', 'Size', 'vector3', 5, default=(1.0, 1.0, 1.0)),
    ],
    'ModePlaneSource': [
        AttributeDef('name', 'Name', 'string', 10),
        AttributeDef('direction', 'Direction', 'select', 10, options=['+', '-'], default='+'),
        AttributeDef('mode_index', 'Mode Index', 'number', 10, default=0),
        AttributeDef('filter_pol', 'Filter Polarization', 'select', 9, options=['te', 'tm', None], default=None),
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

import ast
import os
import sys

def _get_fdtdx_source_files():
    import fdtdx
    base_dir = os.path.dirname(fdtdx.__file__)
    files = []
    for root, _, fnames in os.walk(base_dir):
        for fname in fnames:
            if fname.endswith('.py'):
                files.append(os.path.join(root, fname))
    return files

def _parse_docstrings_from_file(filepath):
    docstrings = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            tree = ast.parse(source)
    except Exception:
        return docstrings

    lines = source.split('\n')
    class_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    
    for cls_node in class_nodes:
        cls_docstrings = {}
        for stmt in cls_node.body:
            if isinstance(stmt, ast.AnnAssign):
                if isinstance(stmt.target, ast.Name):
                    attr_name = stmt.target.id
                    stmt_lineno = stmt.lineno
                    
                    doc_lines = []
                    for line_idx in range(stmt_lineno - 2, -1, -1):
                        # Ensure we don't go out of bounds
                        if line_idx >= len(lines):
                            continue
                        line = lines[line_idx].strip()
                        if line.startswith('#:'):
                            doc_lines.insert(0, line[2:].strip())
                        elif not line:
                            pass
                        elif line.startswith('#'):
                            # Stop at other comments
                            break
                        else:
                            break
                    
                    # Also check inline comments
                    if not doc_lines and line_idx < len(lines):
                        inline_line = lines[stmt_lineno - 1]
                        if '#' in inline_line and not inline_line.strip().startswith('#'):
                            inline_comment = inline_line.split('#', 1)[1].strip()
                            if inline_comment.startswith(':'):
                                doc_lines.append(inline_comment[1:].strip())

                    if doc_lines:
                        cls_docstrings[attr_name] = " ".join(doc_lines)
            
            elif isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        attr_name = target.id
                        stmt_lineno = stmt.lineno
                        doc_lines = []
                        for line_idx in range(stmt_lineno - 2, -1, -1):
                            if line_idx >= len(lines):
                                continue
                            line = lines[line_idx].strip()
                            if line.startswith('#:'):
                                doc_lines.insert(0, line[2:].strip())
                            elif not line:
                                pass
                            elif line.startswith('#'):
                                break
                            else:
                                break
                        if doc_lines:
                            cls_docstrings[attr_name] = " ".join(doc_lines)
        if cls_docstrings:
            docstrings[cls_node.name] = cls_docstrings
    return docstrings

def extract_all_fdtdx_docstrings():
    all_docs = {}
    for filepath in _get_fdtdx_source_files():
        file_docs = _parse_docstrings_from_file(filepath)
        for cls_name, docs in file_docs.items():
            if cls_name not in all_docs:
                all_docs[cls_name] = docs
            else:
                all_docs[cls_name].update(docs)
    return all_docs


# Supplemental tooltips for attributes that have no #: docstrings in the fdtdx source
_SUPPLEMENTAL_TOOLTIPS = {
    'azimuth_angle': 'Azimuth angle of the source in degrees (rotation around vertical axis).',
    'elevation_angle': 'Elevation angle of the source in degrees (tilt from horizontal plane).',
    'static_amplitude_factor': 'Static scaling factor applied to the source amplitude.',
    'radius': 'Radius of the Gaussian beam profile.',
    'std': 'Standard deviation of the Gaussian envelope, relative to radius.',
    'fixed_E_polarization_vector': 'Fixed electric field polarization direction vector (x, y, z).',
    'fixed_H_polarization_vector': 'Fixed magnetic field polarization direction vector (x, y, z).',
    'normalize_by_energy': 'If True, normalize the source by its total energy.',
    'max_angle_random_offset': 'Maximum random angular offset added to azimuth/elevation each step.',
    'max_horizontal_offset': 'Maximum random horizontal offset applied to the source center.',
    'name': 'Unique identifier name for this object.',
    'color': 'Display color for this object in the 3D view.',
    'partial_real_position': 'Position of the object in real (physical) units (x, y, z).',
    'partial_real_shape': 'Shape/size of the object in real (physical) units (x, y, z).',
    'mode_index': 'Index of the waveguide mode to use for this source.',
    'filter_pol': 'Polarization filter to apply (te, tm, or None for both).',
    'plot': 'Whether to generate plots from detector data after simulation.',
    'reduce_volume': 'If True, reduce data to a lower-dimensional slice before saving.',
    'plot_dpi': 'DPI (resolution) of generated plots.',
    'components': 'Field components to record (Ex, Ey, Ez, Hx, Hy, Hz).',
    'num_time_steps_recorded': 'Number of time steps to record. None records all.',
    'dtype': 'Numerical precision for storing detector data.',
    'exact_interpolation': 'Use exact (slower) interpolation when mapping to detector grid.',
    'inverse': 'If True, run detector in inverse/adjoint mode.',
    'if_inverse_plot_backwards': 'If True, reverse time axis in inverse mode plots.',
    'num_video_workers': 'Number of parallel workers for video export (0 = auto).',
    'plot_interpolation': 'Interpolation method used in plot rendering (e.g. gaussian, bilinear).',
    'material': 'Material assigned to this object (defines permittivity/permeability).',
    'as_slices': 'If True, record 2D slices instead of the full 3D volume.',
    'x_slice': 'Position of the X-axis slice when as_slices=True.',
    'y_slice': 'Position of the Y-axis slice when as_slices=True.',
    'z_slice': 'Position of the Z-axis slice when as_slices=True.',
    'direction': 'Propagation direction along the axis (+ or -).',
    'fixed_propagation_axis': 'Axis index (0=x, 1=y, 2=z) for fixed propagation direction.',
    'keep_all_components': 'If True, retain all field components in the output.',
    'wave_character': 'Wave character type (standing, forward, backward).',
    'start_time': 'Time (in seconds) when the switch turns on.',
    'start_after_periods': 'Number of periods after which to turn on.',
    'end_time': 'Time (in seconds) when the switch turns off.',
    'end_after_periods': 'Number of periods after which to turn off.',
    'on_for_time': 'Duration (in seconds) to remain on.',
    'on_for_periods': 'Number of periods to remain on.',
    'period': 'Repetition period of the on/off switching cycle.',
    'interval': 'Number of repeated on/off cycles.',
    'is_always_off': 'If True, the object is permanently disabled (always off).',
    'phase_shift': 'Phase offset applied to the temporal waveform (in radians).',
    'wavelength': 'Free-space wavelength of the wave (in meters).',
    'frequency': 'Frequency of the wave (in Hz).',
    'center_frequency': 'Center frequency of the Gaussian pulse spectrum (in Hz).',
    'spectral_width': 'Spectral width (bandwidth) of the Gaussian pulse (in Hz).',
    'num_startup_periods': 'Number of periods for gradual startup (ramping) of the source.',
}

def populate_tooltips():
    try:
        all_docs = extract_all_fdtdx_docstrings()
        # Flatten: build a global attr_name -> doc lookup across all classes
        global_attr_docs = {}
        for cls_docs in all_docs.values():
            for attr_name, doc in cls_docs.items():
                if attr_name not in global_attr_docs:
                    global_attr_docs[attr_name] = doc
        
        for obj_name, defs in OBJECT_DEFINITIONS.items():
            # First, try to match on the exact class name
            cls_docs = all_docs.get(obj_name, {})
            for attr_def in defs:
                if attr_def.name in cls_docs:
                    attr_def.tooltip = cls_docs[attr_def.name]
                elif attr_def.name in global_attr_docs:
                    # Search across all parsed classes for the attribute
                    attr_def.tooltip = global_attr_docs[attr_def.name]
                elif attr_def.name in _SUPPLEMENTAL_TOOLTIPS:
                    # Final fallback to supplemental dict for un-documented attrs
                    attr_def.tooltip = _SUPPLEMENTAL_TOOLTIPS[attr_def.name]
                         
    except Exception as e:
        print(f"Warning: Failed to parse dynamic tooltips: {e}")
        # In case of any error, use supplemental tooltips as best-effort fallback
        for obj_name, defs in OBJECT_DEFINITIONS.items():
            for attr_def in defs:
                if not attr_def.tooltip and attr_def.name in _SUPPLEMENTAL_TOOLTIPS:
                    attr_def.tooltip = _SUPPLEMENTAL_TOOLTIPS[attr_def.name]

populate_tooltips()
