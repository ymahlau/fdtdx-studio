import json

import fdtdx
from fdtdx.conversion.json import export_json
from fdtdx.objects.boundaries.perfectly_matched_layer import PerfectlyMatchedLayer
from fdtdx.objects.detectors.energy import EnergyDetector
from fdtdx.objects.detectors.field import FieldDetector
from fdtdx.objects.detectors.mode import ModeOverlapDetector
from fdtdx.objects.detectors.phasor import PhasorDetector
from fdtdx.objects.detectors.poynting_flux import PoyntingFluxDetector
from fdtdx.objects.sources.linear_polarization import GaussianPlaneSource
from fdtdx.objects.sources.mode import ModePlaneSource
from fdtdx.objects.sources.profile import SingleFrequencyProfile
from fdtdx.objects.static_material.static import UniformMaterialObject
from nicegui import ui


# Contains all functions responsible for building and exporting the contents of the scene into JSON Files
class Export:
    def __init__(self, Project):
        self.project = Project

    def _clean_nulls(self, obj):
        """
        Recursively traverses lists and dictionaries to remove objects
        of type 'Null' that are not JSON serializable.
        """
        if isinstance(obj, dict):
            return {k: self._clean_nulls(v) for k, v in obj.items() if type(v).__name__ != "Null"}
        elif isinstance(obj, list):
            return [self._clean_nulls(v) for v in obj if type(v).__name__ != "Null"]
        return obj

    def build_export(self):
        """first builds the Simulation Volume and the Simulation Config, then iterates over the objectlist and calls appropiate builder function for object type"""
        cfg = []
        cfg.append(self.build_config())
        cfg.append(self.build_Volume(self.project.objects[0]))
        for obj in self.project.objects[1:]:
            match obj:
                case UniformMaterialObject():
                    cfg.append(self.build_Object(obj))
                case ModePlaneSource():
                    cfg.append(self.build_source(obj))
                case GaussianPlaneSource():
                    cfg.append(self.build_source(obj))
                case (
                    EnergyDetector()
                    | FieldDetector()
                    | ModeOverlapDetector()
                    | PhasorDetector()
                    | PoyntingFluxDetector()
                ):
                    cfg.append(self.build_detector(obj))
                case PerfectlyMatchedLayer():
                    cfg.append(export_json(obj))
        if self.project.model.constraints:
            for key, value in self.project.model.constraints.items():
                cfg.append(self.build_constraint(key, value))
        return cfg

    def export(self):
        """Creates the config.json and cleans data before dumping"""
        raw_cfg = self.build_export()
        clean_cfg = self._clean_nulls(raw_cfg)

        ui.download.content(json.dumps(clean_cfg, indent=4), self.project.name.__add__(".json"))
        ui.notify("Config Saved")

    def export_material_list(self, list_obj):
        """Applies cleaning before downloading material list"""
        raw_cfg = self.build_material_list(list_obj)
        clean_cfg = self._clean_nulls(raw_cfg)

        ui.download.content(json.dumps(clean_cfg, indent=4), "material_list.json")
        ui.notify("Material List saved")

    def build_material_list(self, list_obj):
        """builds the JSON serializable output of all Nonstandard Materials that were defined, calls build material for each"""
        cfg = []
        for obj in list_obj:
            material, name, editable = obj
            if editable:
                cfg.append(self.build_material(material, name))
        return cfg

    def build_config(self):
        """Specifies the config.json"""
        return {
            "__module__": "fdtdx.config",
            "__name__": "SimulationConfig",
            "backend": self.project.param.backend,
            "courant_factor": self.project.param.courant_factor,
            "dtype": {"__dtype__": self.project.param.dtype.value},
            "gradient_config": "NULL",
            "resolution": self.project.param.resolution,
            "time": self.project.param.time,
        }

    def build_Volume(self, Volume: fdtdx.SimulationVolume):
        """builds JSON text for the simulation Volume"""
        return {
            "__module__": "fdtdx.objects.static_material.static",
            "__name__": "SimulationVolume",
            "partial_real_shape": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": Volume.partial_real_shape,
            },
            "material": {
                "__module__": "fdtdx.materials",
                "electric_conductivity": Volume.material.electric_conductivity,
                "magnetic_conductivity": Volume.material.magnetic_conductivity,
                "permeability": Volume.material.permeability,
                "permittivity": Volume.material.permittivity,
                "__name__": self.project.model.material.get_name_from_material(Volume.material),
            },
        }

    # Builds JSON text for UniformMaterialObjects
    def build_Object(self, Object: fdtdx.UniformMaterialObject):
        return {
            "__module__": "fdtdx.objects.static_material.static",
            "__name__": "UniformMaterialObject",
            "color": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": self.hex_to_RGB(Object.color) if isinstance(Object.color, str) else Object.color,
            },
            "material": {
                "__module__": "fdtdx.materials",
                "__name__": self.project.model.material.get_name_from_material(Object.material),
                "electric_conductivity": Object.material.electric_conductivity,
                "magnetic_conductivity": Object.material.magnetic_conductivity,
                "permeability": Object.material.permeability,
                "permittivity": Object.material.permittivity,
            },
            "max_random_grid_offsets": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": Object.max_random_grid_offsets,
            },
            "max_random_real_offsets": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": Object.max_random_real_offsets,
            },
            "name": Object.name,
            "partial_grid_shape": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": Object.partial_grid_shape,
            },
            "partial_real_position": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": Object.partial_real_position,
            },
            "partial_real_shape": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": Object.partial_real_shape,
            },
            "placement_order": Object.placement_order,
        }

    # Builds JSON text from Material
    def build_material(self, obj: fdtdx.Material, name: str):
        return {
            "__module__": "fdtdx.materials",
            "__name__": name,
            "electric_conductivity": obj.electric_conductivity,
            "magnetic_conductivity": obj.magnetic_conductivity,
            "permeability": obj.permeability,
            "permittivity": obj.permittivity,
        }

    # Builds JSON text for sources with only the options expected for each type
    def build_source(self, obj):
        is_mode_source = isinstance(obj, ModePlaneSource)

        ret = {
            "__module__": "fdtdx.objects.sources.mode"
            if is_mode_source
            else "fdtdx.objects.sources.linear_polarization",
            "__name__": "ModePlaneSource" if is_mode_source else "GaussianPlaneSource",
            "azimuth_angle": obj.azimuth_angle,
            "color": {
                "__module__": "builtins",
                "__name__": "tuple",
                "__value__": self.hex_to_RGB(obj.color) if isinstance(obj.color, str) else obj.color,
            },
            "direction": obj.direction,
            "elevation_angle": obj.elevation_angle,
        }

        if is_mode_source:
            ret.update({"filter_pol": obj.filter_pol, "mode_index": obj.mode_index})
        else:
            ret.update(
                {
                    "fixed_E_polarization_vector": obj.fixed_E_polarization_vector,
                    "fixed_H_polarization_vector": obj.fixed_H_polarization_vector,
                    "normalize_by_energy": obj.normalize_by_energy,
                    "radius": obj.radius,
                    "std": obj.std,
                }
            )

        ret.update(
            {
                "max_angle_random_offset": obj.max_angle_random_offset,
                "max_horizontal_offset": obj.max_horizontal_offset,
                "max_random_grid_offsets": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.max_random_grid_offsets,
                },
                "max_random_real_offsets": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.max_random_real_offsets,
                },
                "max_vertical_offset": obj.max_vertical_offset,
                "name": obj.name,
                "partial_grid_shape": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.partial_grid_shape,
                },
                "partial_real_shape": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.partial_real_shape,
                },
                "static_amplitude_factor": obj.static_amplitude_factor,
            }
        )

        ret.update(
            {
                "switch": {
                    "__module__": "fdtdx.core.switch",
                    "__name__": "OnOffSwitch",
                    "end_after_periods": obj.switch.end_after_periods,
                    "end_time": obj.switch.end_time,
                    "fixed_on_time_steps": obj.switch.fixed_on_time_steps,
                    "interval": obj.switch.interval,
                    "is_always_off": obj.switch.is_always_off,
                    "on_for_periods": obj.switch.on_for_periods,
                    "on_for_time": obj.switch.on_for_time,
                    "period": obj.switch.period,
                    "start_after_periods": obj.switch.start_after_periods,
                    "start_time": obj.switch.start_time,
                }
            }
        )

        if isinstance(obj.temporal_profile, SingleFrequencyProfile):
            ret.update(
                {
                    "temporal_profile": {
                        "__module__": "fdtdx.objects.sources.profile",
                        "__name__": "SingleFrequencyProfile",
                        "num_startup_periods": obj.temporal_profile.num_startup_periods,
                        "phase_shift": obj.temporal_profile.phase_shift,
                    }
                }
            )
        else:
            ret.update(
                {
                    "temporal_profile": {
                        "__module__": "fdtdx.objects.sources.profile",
                        "__name__": "GaussianPulseProfile",
                        "spectral_width": obj.temporal_profile.spectral_width,
                        "center_frequency": obj.temporal_profile.center_frequency,
                    }
                }
            )

        ret.update(
            {
                "wave_character": {
                    "__module__": "fdtdx.core.wavelength",
                    "__name__": "WaveCharacter",
                    "frequency": obj.wave_character.frequency,
                    "period": obj.wave_character.period,
                    "phase_shift": obj.wave_character.phase_shift,
                    "wavelength": obj.wave_character.wavelength,
                },
                "partial_real_position": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.partial_real_position,
                },
            }
        )
        return ret

    # Builds JSON text for detectors with only the options expected for each type
    def build_detector(self, obj):
        result = {}
        match obj:
            case EnergyDetector():
                result.update(
                    {
                        "__module__": "fdtdx.objects.detectors.energy",
                        "__name__": "EnergyDetector",
                        "aggregate": obj.aggregate,
                        "as_slices": obj.as_slices,
                    }
                )
            case FieldDetector():
                result.update({"__module__": "fdtdx.objects.detectors.field", "__name__": "FieldDetector"})
            case ModeOverlapDetector():
                result.update({"__module__": "fdtdx.objects.detectors.mode", "__name__": "ModeOverlapDetector"})
            case PhasorDetector():
                result.update({"__module__": "fdtdx.objects.detectors.phasor", "__name__": "PhasorDetector"})
            case PoyntingFluxDetector():
                result.update(
                    {"__module__": "fdtdx.objects.detectors.poynting_flux", "__name__": "PoyntingFluxDetector"}
                )

        result.update(
            {
                "color": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": self.hex_to_RGB(obj.color) if isinstance(obj.color, str) else obj.color,
                }
            }
        )

        match obj:
            case EnergyDetector():
                None
            case FieldDetector() | PhasorDetector():
                result.update(
                    {"components": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.components}}
                )
            case ModeOverlapDetector() | PoyntingFluxDetector():
                result.update({"direction": obj.direction})

        result.update({"dtype": {"__dtype__": "jax.numpy.float32"}, "exact_interpolation": obj.exact_interpolation})

        match obj:
            case ModeOverlapDetector():
                result.update(
                    {
                        "filter_pol": obj.filter_pol,
                        "if_inverse_plot_backwards": obj.if_inverse_plot_backwards,
                        "inverse": obj.inverse,
                    }
                )
            case PoyntingFluxDetector():
                result.update(
                    {
                        "fixed_propagation_axis": obj.fixed_propagation_axis,
                        "if_inverse_plot_backwards": obj.if_inverse_plot_backwards,
                        "inverse": obj.inverse,
                        "keep_all_components": obj.keep_all_components,
                    }
                )
            case _:
                result.update({"if_inverse_plot_backwards": obj.if_inverse_plot_backwards, "inverse": obj.inverse})

        result.update(
            {
                "max_random_grid_offsets": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.max_random_grid_offsets,
                },
                "max_random_real_offsets": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.max_random_real_offsets,
                },
            }
        )

        if isinstance(obj, ModeOverlapDetector):
            result.update({"mode_index": obj.mode_index})

        result.update(
            {
                "name": obj.name,
                "num_video_workers": obj.num_video_workers,
                "partial_grid_shape": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.partial_grid_shape,
                },
                "partial_real_shape": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.partial_real_shape,
                },
                "partial_real_position": {
                    "__module__": "builtins",
                    "__name__": "tuple",
                    "__value__": obj.partial_real_position,
                },
            }
        )

        if not isinstance(obj, ModeOverlapDetector):
            result.update({"plot": obj.plot})

        result.update({"plot_dpi": obj.plot_dpi, "plot_interpolation": obj.plot_interpolation})

        if not isinstance(obj, ModeOverlapDetector):
            result.update({"reduce_volume": obj.reduce_volume})

        result.update(
            {
                "switch": {
                    "__module__": "fdtdx.core.switch",
                    "__name__": "OnOffSwitch",
                    "end_after_periods": obj.switch.end_after_periods,
                    "end_time": obj.switch.end_time,
                    "fixed_on_time_steps": obj.switch.fixed_on_time_steps,
                    "interval": obj.switch.interval,
                    "is_always_off": obj.switch.is_always_off,
                    "on_for_periods": obj.switch.on_for_periods,
                    "on_for_time": obj.switch.on_for_time,
                    "period": obj.switch.period,
                    "start_after_periods": obj.switch.start_after_periods,
                    "start_time": obj.switch.start_time,
                }
            }
        )

        match obj:
            case EnergyDetector():
                result.update({"x_slice": obj.x_slice, "y_slice": obj.y_slice, "z_slice": obj.z_slice})
            case FieldDetector() | PhasorDetector():
                result.update(
                    {
                        "wave_characters": {
                            "__module__": "builtins",
                            "__name__": "list",
                            "__value__": obj.wave_characters,
                        }
                    }
                )
            case _:
                pass

        return result

    # Builds JSON text for contraints with only the options expected for each type
    def build_constraint(self, key, value):
        obj = value
        result = {"__module__": "fdtdx.constraints", "key": key, "object": obj.object}
        match type(obj):
            case fdtdx.PositionConstraint:
                result.update(
                    {
                        "__name__": "PositionConstraint",
                        "other_object": obj.other_object,
                        "axes": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.axes},
                        "object_positions": {
                            "__module__": "builtins",
                            "__name__": "tuple",
                            "__value__": obj.object_positions,
                        },
                        "other_object_positions": {
                            "__module__": "builtins",
                            "__name__": "tuple",
                            "__value__": obj.other_object_positions,
                        },
                        "margins": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.margins},
                        "grid_margins": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.grid_margins},
                    }
                )
            case fdtdx.SizeConstraint:
                result.update(
                    {
                        "__name__": "SizeConstraint",
                        "other_object": obj.other_object,
                        "axes": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.axes},
                        "other_axes": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.other_axes},
                        "proportions": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.proportions},
                        "offsets": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.offsets},
                        "grid_offsets": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.grid_offsets},
                    }
                )
            case fdtdx.SizeExtensionConstraint:
                result.update(
                    {
                        "__name__": "SizeExtensionConstraint",
                        "other_object": obj.other_object,
                        "axis": obj.axis,
                        "direction": obj.direction,
                        "other_position": obj.other_position,
                        "offset": obj.offset,
                        "grid_offset": obj.grid_offset,
                    }
                )
            case fdtdx.GridCoordinateConstraint:
                result.update(
                    {
                        "__name__": "GridCoordinateConstraint",
                        "axes": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.axes},
                        "sides": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.sides},
                        "coordinates": {"__module__": "builtins", "__name__": "tuple", "__value__": obj.coordinates},
                    }
                )
        return result

    # check if colour should be in 0 to 1 range or in 0 to 255
    def hex_to_RGB(self, hex_color: str):
        if "#" in hex_color:
            """Convert hex color string (e.g. 'FF0000') to normalized RGB tuple (0-1 range)"""
            # Remove '#' if present
            hex_color = hex_color.lstrip("#")

            # Convert hex to RGB (0-255)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            # Normalize to 0-1 range
            return (r / 255.0, g / 255.0, b / 255.0)
        else:
            return hex_color

    @staticmethod
    def exists_on_client():
        return None
