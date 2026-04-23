from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class AttributeDef:
    name: str
    label: str
    ui_type: str  # 'number', 'string', 'boolean', 'select', 'color', 'nested', 'vector3'
    importance: int  # > 0 means visible by default
    default: Any = None
    options: Optional[List[Any]] = None  # For 'select' type
    tooltip: Optional[str] = None
    target_cls: Optional[str] = None  # For 'nested' type, the class of the nested object


# Metadata definitions for fdtdx objects
OBJECT_DEFINITIONS: Dict[str, List[AttributeDef]] = {
    "GaussianPlaneSource": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("direction", "Direction", "select", 10, options=["+", "-"], default="+"),
        AttributeDef("azimuth_angle", "Azimuth Angle", "number", 9, default=0.0),
        AttributeDef("elevation_angle", "Elevation Angle", "number", 9, default=0.0),
        AttributeDef("static_amplitude_factor", "Amplitude Factor", "number", 8, default=1.0),
        AttributeDef("color", "Color", "color", 8, default="#FF0000"),
        AttributeDef("temporal_profile", "Temporal Profile", "nested", 7, target_cls="TemporalProfile"),
        AttributeDef("switch", "Switch", "nested", 6, target_cls="OnOffSwitch"),
        AttributeDef("wave_character", "Wave Character", "nested", 6, target_cls="WaveCharacter"),
        # New attributes
        AttributeDef("fixed_E_polarization_vector", "Fixed E Polarization", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("fixed_H_polarization_vector", "Fixed H Polarization", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("normalize_by_energy", "Normalize by Energy", "boolean", 5, default=True),
        AttributeDef("radius", "Radius", "number", 5, default=0.0),
        AttributeDef("std", "Standard Deviation", "number", 5, default=0.33),
        AttributeDef("max_angle_random_offset", "Max Angle Random Offset", "number", 0, default=0.0),
        AttributeDef("max_horizontal_offset", "Max Horizontal Offset", "number", 0, default=0.0),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
    ],
    "ModePlaneSource": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("direction", "Direction", "select", 10, options=["+", "-"], default="+"),
        AttributeDef("mode_index", "Mode Index", "number", 10, default=0),
        AttributeDef("filter_pol", "Filter Polarization", "select", 9, options=["te", "tm", None], default=None),
        AttributeDef("temporal_profile", "Temporal Profile", "nested", 8, target_cls="TemporalProfile"),
        AttributeDef("switch", "Switch", "nested", 6, target_cls="OnOffSwitch"),
        AttributeDef("wave_character", "Wave Character", "nested", 6, target_cls="WaveCharacter"),
        AttributeDef("color", "Color", "color", 8, default="#0000FF"),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
    ],
    "UniformMaterialObject": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("material", "Material", "material_select", 10),
        AttributeDef("color", "Color", "color", 10, default="#808080"),
        AttributeDef("partial_real_position", "Position", "vector3", 10, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 10, default=(1.0, 1.0, 1.0)),
    ],
    "FieldDetector": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("plot", "Plot", "boolean", 9, default=False),
        AttributeDef("reduce_volume", "Reduce Volume", "boolean", 8, default=False),
        AttributeDef("plot_dpi", "Plot DPI", "number", 7, default=100),
        AttributeDef(
            "components",
            "Components",
            "multi_select",
            9,
            options=["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"],
            default=["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"],
        ),
        AttributeDef("num_time_steps_recorded", "Num Time Steps Recorded", "number", 5),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
        AttributeDef("color", "Color", "color", 5, default="#00FF00"),
        AttributeDef("switch", "Switch", "nested", 4, target_cls="OnOffSwitch"),
        # Shared detector attributes
        AttributeDef("dtype", "Data Type", "select", 8, options=["float32", "float64"], default="float32"),
        AttributeDef("exact_interpolation", "Exact Interpolation", "boolean", 0, default=False),
        AttributeDef("inverse", "Inverse", "boolean", 0, default=False),
        AttributeDef("if_inverse_plot_backwards", "Inverse Plot Backwards", "boolean", 0, default=False),
        AttributeDef("num_video_workers", "Num Video Workers", "number", 0, default=0),
        AttributeDef("plot_interpolation", "Plot Interpolation", "string", 0, default="gaussian"),
    ],
    "EnergyDetector": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("plot_dpi", "Plot DPI", "number", 8, default=100),
        AttributeDef("as_slices", "As Slices", "boolean", 9, default=False),
        AttributeDef("x_slice", "X Slice", "number", 7, default=0.0),
        AttributeDef("y_slice", "Y Slice", "number", 7, default=0.0),
        AttributeDef("z_slice", "Z Slice", "number", 7, default=0.0),
        AttributeDef("reduce_volume", "Reduce Volume", "boolean", 5, default=False),
        AttributeDef("color", "Color", "color", 5, default="#FFFF00"),
        AttributeDef("switch", "Switch", "nested", 4, target_cls="OnOffSwitch"),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef("dtype", "Data Type", "select", 8, options=["float32", "float64"], default="float32"),
        AttributeDef("exact_interpolation", "Exact Interpolation", "boolean", 0, default=False),
        AttributeDef("inverse", "Inverse", "boolean", 0, default=False),
        AttributeDef("if_inverse_plot_backwards", "Inverse Plot Backwards", "boolean", 0, default=False),
        AttributeDef("num_video_workers", "Num Video Workers", "number", 0, default=0),
        AttributeDef("plot_interpolation", "Plot Interpolation", "string", 0, default="gaussian"),
    ],
    "PoyntingFluxDetector": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("direction", "Direction", "select", 9, options=["+", "-"], default="+"),
        AttributeDef("fixed_propagation_axis", "Fixed Prop Axis", "number", 9, default=0),
        AttributeDef("keep_all_components", "Keep All Components", "boolean", 8, default=False),
        AttributeDef("plot_dpi", "Plot DPI", "number", 7, default=100),
        AttributeDef("switch", "Switch", "nested", 4, target_cls="OnOffSwitch"),
        AttributeDef("color", "Color", "color", 5, default="#FFA500"),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef("dtype", "Data Type", "select", 8, options=["float32", "float64"], default="float32"),
        AttributeDef("exact_interpolation", "Exact Interpolation", "boolean", 0, default=False),
        AttributeDef("inverse", "Inverse", "boolean", 0, default=False),
        AttributeDef("if_inverse_plot_backwards", "Inverse Plot Backwards", "boolean", 0, default=False),
        AttributeDef("num_video_workers", "Num Video Workers", "number", 0, default=0),
        AttributeDef("plot_interpolation", "Plot Interpolation", "string", 0, default="gaussian"),
    ],
    "PhasorDetector": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("direction", "Direction", "select", 9, options=["+", "-"], default=None),
        AttributeDef("fixed_propagation_axis", "Fixed Prop Axis", "number", 9, default=None),
        AttributeDef(
            "components", "Components", "multi_select", 9, options=["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"], default=[]
        ),
        AttributeDef("filter_pol", "Filter Pol", "select", 8, options=["h", "v", None], default=None),
        AttributeDef(
            "wave_character",
            "Wave Character",
            "select",
            8,
            options=["standing", "forward", "backward"],
            default="standing",
        ),
        AttributeDef("plot_dpi", "Plot DPI", "number", 7, default=100),
        AttributeDef("switch", "Switch", "nested", 4, target_cls="OnOffSwitch"),
        AttributeDef("color", "Color", "color", 5, default="#00FFFF"),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef("dtype", "Data Type", "select", 8, options=["float32", "float64"], default="float32"),
        AttributeDef("exact_interpolation", "Exact Interpolation", "boolean", 0, default=False),
        AttributeDef("inverse", "Inverse", "boolean", 0, default=False),
        AttributeDef("if_inverse_plot_backwards", "Inverse Plot Backwards", "boolean", 0, default=False),
        AttributeDef("num_video_workers", "Num Video Workers", "number", 0, default=0),
        AttributeDef("plot_interpolation", "Plot Interpolation", "string", 0, default="gaussian"),
    ],
    "ModeOverlapDetector": [
        AttributeDef("name", "Name", "string", 10),
        AttributeDef("direction", "Direction", "select", 9, options=["+", "-"], default="+"),
        AttributeDef("mode_index", "Mode Index", "number", 9, default=0),
        AttributeDef("filter_pol", "Filter Pol", "select", 8, options=["te", "tm", None], default=None),
        AttributeDef("plot_dpi", "Plot DPI", "number", 7, default=100),
        AttributeDef("switch", "Switch", "nested", 4, target_cls="OnOffSwitch"),
        AttributeDef("color", "Color", "color", 5, default="#FF00FF"),
        AttributeDef("partial_real_position", "Position", "vector3", 5, default=(0.0, 0.0, 0.0)),
        AttributeDef("partial_real_shape", "Size", "vector3", 5, default=(1.0, 1.0, 1.0)),
        # Shared detector attributes
        AttributeDef("dtype", "Data Type", "select", 8, options=["float32", "float64"], default="float32"),
        AttributeDef("exact_interpolation", "Exact Interpolation", "boolean", 0, default=False),
        AttributeDef("inverse", "Inverse", "boolean", 0, default=False),
        AttributeDef("if_inverse_plot_backwards", "Inverse Plot Backwards", "boolean", 0, default=False),
        AttributeDef("num_video_workers", "Num Video Workers", "number", 0, default=0),
        AttributeDef("plot_interpolation", "Plot Interpolation", "string", 0, default="gaussian"),
    ],
    "OnOffSwitch": [
        AttributeDef("start_time", "Start Time", "number", 5),
        AttributeDef("start_after_periods", "Start After Periods", "number", 5),
        AttributeDef("end_time", "End Time", "number", 5),
        AttributeDef("end_after_periods", "End After Periods", "number", 5),
        AttributeDef("on_for_time", "On For Time", "number", 5),
        AttributeDef("on_for_periods", "On For Periods", "number", 5),
        AttributeDef("period", "Period", "number", 5),
        AttributeDef("interval", "Interval", "number", 5, default=1),
        AttributeDef("is_always_off", "Always Off", "boolean", 5, default=False),
    ],
    "SingleFrequencyProfile": [
        AttributeDef("phase_shift", "Phase Shift", "number", 10, default=0.0),
        AttributeDef("num_startup_periods", "Num Startup Periods", "number", 10, default=0),
    ],
    "GaussianPulseProfile": [
        AttributeDef("center_frequency", "Center Frequency", "number", 10),
        AttributeDef("spectral_width", "Spectral Width", "number", 10),
        AttributeDef("phase_shift", "Phase Shift", "number", 10),
    ],
    "WaveCharacter": [
        AttributeDef("phase_shift", "Phase Shift", "number", 10, default=0.0),
        AttributeDef("wavelength", "Wavelength", "number", 5),
        AttributeDef("frequency", "Frequency", "number", 5),
        AttributeDef("period", "Period", "number", 5),
    ],
}

import ast
import os


def _get_fdtdx_source_files():
    import fdtdx

    base_dir = os.path.dirname(fdtdx.__file__)
    files = []
    for root, _, fnames in os.walk(base_dir):
        for fname in fnames:
            if fname.endswith(".py"):
                files.append(os.path.join(root, fname))
    return files


def _parse_docstrings_from_file(filepath):
    docstrings = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
            tree = ast.parse(source)
    except Exception:
        return docstrings

    lines = source.split("\n")
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
                        if line.startswith("#:"):
                            doc_lines.insert(0, line[2:].strip())
                        elif not line:
                            pass
                        elif line.startswith("#"):
                            # Stop at other comments
                            break
                        else:
                            break

                    # Also check inline comments
                    if not doc_lines and line_idx < len(lines):
                        inline_line = lines[stmt_lineno - 1]
                        if "#" in inline_line and not inline_line.strip().startswith("#"):
                            inline_comment = inline_line.split("#", 1)[1].strip()
                            if inline_comment.startswith(":"):
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
                            if line.startswith("#:"):
                                doc_lines.insert(0, line[2:].strip())
                            elif not line:
                                pass
                            elif line.startswith("#"):
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


# Fallback tooltips for attributes that have no #: docstrings in the fdtdx source
ATTRIBUTE_TOOLTIP_FALLBACKS: Dict[str, str] = {
    "azimuth_angle": "Azimuth angle of the source in degrees (rotation around vertical axis).",
    "elevation_angle": "Elevation angle of the source in degrees (tilt above/below horizontal).",
    "static_amplitude_factor": "Scalar amplitude multiplier applied to the source field.",
    "max_angle_random_offset": "Maximum random angular offset added to azimuth/elevation (degrees).",
    "max_horizontal_offset": "Maximum random horizontal position offset (physical units).",
    "max_vertical_offset": "Maximum random vertical position offset (physical units).",
    "normalize_by_energy": "If True, normalizes the source field so total energy is 1.",
    "fixed_E_polarization_vector": "Fixed electric field polarization direction (x, y, z). If None, auto-computed.",
    "fixed_H_polarization_vector": "Fixed magnetic field polarization direction (x, y, z). If None, auto-computed.",
    "radius": "Radius of the Gaussian beam in physical units.",
    "std": "Standard deviation of the Gaussian beam profile, relative to the radius.",
    "amplitude": "Scalar amplitude of the source.",
    "mode_index": "Index of the eigenmode to use (0 = fundamental mode).",
    "filter_pol": "Polarization filter applied to the mode (te, tm, or None).",
    "partial_real_position": "Position of the object in physical space (x, y, z).",
    "partial_real_shape": "Size/shape of the object in physical space (x, y, z).",
    "color": "Display color of the object in the 3D viewport.",
    "dtype": "Numerical precision for recorded data (float32 or float64).",
    "exact_interpolation": "If True, uses exact interpolation for detector data. Slower but more accurate.",
    "inverse": "If True, runs detector in inverse/adjoint mode.",
    "if_inverse_plot_backwards": "If True, reverses time axis when plotting inverse data.",
    "num_video_workers": "Number of parallel workers for video export (0 = auto).",
    "plot_interpolation": 'Interpolation method used in 2D detector plots (e.g. "gaussian").',
    "plot_dpi": "Resolution of exported detector plots in dots per inch.",
    "plot": "If True, generates plots for this detector automatically.",
    "reduce_volume": "If True, reduces the detector volume to save memory.",
    "components": "Field components to record (e.g. Ex, Ey, Ez, Hx, Hy, Hz).",
    "num_time_steps_recorded": "Number of time steps to record. None means all steps.",
    "as_slices": "If True, stores detector data as 2D slices instead of a full volume.",
    "x_slice": "X-coordinate of the slice plane (physical units).",
    "y_slice": "Y-coordinate of the slice plane (physical units).",
    "z_slice": "Z-coordinate of the slice plane (physical units).",
    "fixed_propagation_axis": "Fixed axis index for the propagation direction (0=x, 1=y, 2=z).",
    "keep_all_components": "If True, keeps all field components instead of just flux.",
    "direction": "Direction of propagation ('+' or '-' along the propagation axis).",
    "name": "Unique name for this object.",
    "material": "Material assigned to this object.",
    "start_time": "Absolute time at which the source/detector turns on (seconds).",
    "start_after_periods": "Number of wave periods to wait before turning on.",
    "end_time": "Absolute time at which the source/detector turns off (seconds).",
    "end_after_periods": "Number of wave periods after which the source/detector turns off.",
    "on_for_time": "Duration for which the source/detector stays on (seconds).",
    "on_for_periods": "Duration in wave periods for which the source/detector stays on.",
    "period": "Repetition period of the on/off switching cycle (seconds).",
    "interval": "Time step interval between consecutive on-events.",
    "is_always_off": "If True, the source/detector is permanently disabled.",
    "phase_shift": "Phase offset of the wave in radians.",
    "wavelength": "Wavelength of the wave in physical units.",
    "frequency": "Frequency of the wave in Hz.",
    "center_frequency": "Center frequency of the Gaussian pulse in Hz.",
    "spectral_width": "Spectral width (bandwidth) of the Gaussian pulse in Hz.",
    "num_startup_periods": "Number of ramp-up periods before the source reaches full amplitude.",
}

ALL_DOCS: Dict[str, Dict[str, str]] = {}


def populate_tooltips():
    global ALL_DOCS
    try:
        all_docs = extract_all_fdtdx_docstrings()
        ALL_DOCS.update(all_docs)

        # Build a flat attribute-name -> docstring fallback map across all classes
        attr_fallback: Dict[str, str] = {}
        for cls_docs in all_docs.values():
            for attr_name, doc in cls_docs.items():
                if attr_name not in attr_fallback:
                    attr_fallback[attr_name] = doc

        for obj_name, defs in OBJECT_DEFINITIONS.items():
            # First pass: match from the exact class definition
            cls_docs = all_docs.get(obj_name, {})
            for attr_def in defs:
                if attr_def.name in cls_docs:
                    attr_def.tooltip = cls_docs[attr_def.name]

            # Second pass: fallback to any class that has that attribute documented
            for attr_def in defs:
                if not attr_def.tooltip and attr_def.name in attr_fallback:
                    attr_def.tooltip = attr_fallback[attr_def.name]

            # Third pass: use the static fallback dictionary
            for attr_def in defs:
                if not attr_def.tooltip and attr_def.name in ATTRIBUTE_TOOLTIP_FALLBACKS:
                    attr_def.tooltip = ATTRIBUTE_TOOLTIP_FALLBACKS[attr_def.name]

    except Exception as e:
        print(f"Warning: Failed to parse dynamic tooltips: {e}")


populate_tooltips()
