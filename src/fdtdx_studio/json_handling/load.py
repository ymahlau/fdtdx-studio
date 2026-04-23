import json
from typing import Any

import fdtdx

from fdtdx_studio.parameter.datatypes.model import Model
from fdtdx_studio.parameter.dtype import DType


class Import:

  def __init__(self, Project,controller):
    self.project = Project
    self.controller = controller


  #Converts RGB values between 0-1 to standard hex color codes
  def RGB_to_hex(self, color):
    return f"#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}"

  #imports uniform material objects
  def import_UMO(self,obj):
    matName = obj['material'].get('__name__', 'Unknown Material')
    try:
      material = self.project.model.material.get_material_from_settings(permittivity= obj['material']['permittivity'],
                                                                       permeability= obj['material']['permeability'],
                                                                       e_conductivity= obj['material']['electric_conductivity'],
                                                                       m_conductivity= obj['material']['magnetic_conductivity'],
                                                                       name= matName)
    except Exception as e:
      raise Exception(f"Import error: could not find material ‚{matName}")

    self.project.model.create_material_obj(
        name = obj['name'],
        partial_grid_shape = obj['partial_grid_shape']['__value__'],
        partial_real_position= obj['partial_real_position']['__value__'],
        partial_real_shape = obj['partial_real_shape']['__value__'],
        color = self.RGB_to_hex(obj['color']['__value__']),
        material= self.project.model.material.get_material_from_settings(permittivity= obj['material']['permittivity'],
                                                                       permeability= obj['material']['permeability'],
                                                                       e_conductivity= obj['material']['electric_conductivity'],
                                                                       m_conductivity= obj['material']['magnetic_conductivity'],
                                                                       name= obj['material'].get('__name__', 'Unknown Material')),
        max_random_grid_offsets = obj['max_random_grid_offsets']['__value__'],
        max_random_real_offsets = obj['max_random_real_offsets']['__value__']
      )
  
  #imports All sources and creates the correct kind of source depending on the type
  def import_Source(self,obj):
    # pop all key value pairs from the dictionary that are not needed and not expected by the importer
    obj['wave_character'].pop("__module__")
    obj['wave_character'].pop("__name__")
    obj['switch'].pop("__module__")
    obj['switch'].pop("__name__")
    obj['temporal_profile'].pop("__module__")
    obj['temporal_profile'].update({"type": obj['temporal_profile'].pop("__name__")})
    if(obj['__name__']=='ModePlaneSource'):
      self.controller.add_mode_source(
        project= self.project,
        typ = obj['__name__'],
        name= obj['name'],
        partial_real_shape = obj['partial_real_shape']['__value__'],
        color=self.RGB_to_hex(obj['color']['__value__']),
        direction=obj['direction'],
        wave = obj['wave_character'],
        azimuth_angle = obj['azimuth_angle'],
        elevation_angle = obj['elevation_angle'],
        temporal_profile = obj['temporal_profile'],
        switch = obj['switch'],
        filter_pol = obj['filter_pol'],
        mode_index = obj['mode_index'],
        partial_real_position = obj['partial_real_position']['__value__']
      )
    elif obj['__name__']=='GaussianPlaneSource':
      self.controller.add_gaussian_source(
        project = self.project,
        typ = obj['__name__'],
        name= obj['name'],
        partial_real_shape = obj['partial_real_shape']['__value__'],
        color=self.RGB_to_hex(obj['color']['__value__']),
        direction=obj['direction'],
        wave = obj['wave_character'],
        azimuth_angle = obj['azimuth_angle'],
        elevation_angle = obj['elevation_angle'],
        temporal_profile = obj['temporal_profile'],
        switch = obj['switch'],
        fixed_E_polarization_vector = obj['fixed_E_polarization_vector'],
        fixed_H_polarization_vector = obj['fixed_H_polarization_vector'],
        normalize_by_energy = obj['normalize_by_energy'],
        radius = obj['radius'],
        std = obj['std'],
        partial_real_position = obj['partial_real_position']['__value__']
      )
    else:
      None

  #imports All Detectors and creates the correct kind of detector depending on the type
  def import_Detector(self,obj):
    type = obj['__name__']
    arguments = {
      'dtype': "jax.numpy.float32", #TODO
      'exact_interpolation': obj['exact_interpolation'],
      'inverse': obj['inverse'],
      'switch': fdtdx.OnOffSwitch(
        start_time= obj['switch']['start_time'],
        start_after_periods= obj['switch']['start_after_periods'],
        end_time= obj['switch']['end_time'],
        end_after_periods= obj['switch']['end_after_periods'],
        on_for_time= obj['switch']['on_for_time'],
        on_for_periods= obj['switch']['on_for_periods'],
        period= obj['switch']['period'],
        fixed_on_time_steps= obj['switch']['fixed_on_time_steps'],
        is_always_off= obj['switch']['is_always_off'],
        interval= obj['switch']['interval']
      ),
      'if_inverse_plot_backwards': obj['if_inverse_plot_backwards'],
      'num_video_workers': obj['num_video_workers'],
      'color': self.RGB_to_hex(obj['color']['__value__']),
      'plot_interpolation': obj['plot_interpolation'],
      'plot_dpi': obj['plot_dpi'],
      'max_random_grid_offsets': obj['max_random_grid_offsets']['__value__'],
      'max_random_real_offsets': obj['max_random_real_offsets']['__value__'],
      'partial_grid_shape': obj['partial_grid_shape']['__value__'],
      'partial_real_shape':obj['partial_real_shape']['__value__'],
      'partial_real_position': obj['partial_real_position']['__value__'],
      'name': obj['name']
    }
    match type:
      case 'EnergyDetector':
        arguments.update({
          'as_slices': obj['as_slices'],
          'reduce_volume': obj['reduce_volume'],
          'x_slice': obj['x_slice'],
          'y_slice': obj['y_slice'],
          'z_slice': obj['z_slice'],
          'aggregate': obj['aggregate']
        })
        self.project.model.create_energy_detector_obj(**arguments)
      case 'FieldDetector':
        arguments.update({
          'reduce_volume': obj['reduce_volume'],
          'components': obj['components']['__value__']
        })
        self.project.model.create_field_detector_obj(**arguments)
      case 'ModeOverlapDetector':
        arguments.update({
          'direction': obj['direction'],
          'mode_index': obj['mode_index'],
          'filter_pol': obj['filter_pol'],
        })
        self.project.model.create_mode_overlap_detector(**arguments)
      case 'PhasorDetector':
        arguments.update({
          'wave_characters': obj['wave_characters']['__value__'],
          'reduce_volume': obj['reduce_volume'],
          'components': obj['components']['__value__']
        })
        self.project.model.create_phasor_detector(**arguments)
      case 'PoyntingFluxDetector':
        arguments.update({
          'direction': obj['direction'],
          'reduce_volume': obj['reduce_volume'],
          'fixed_propagation_axis': obj['fixed_propagation_axis'],
          'keep_all_components': obj['keep_all_components']
        })
        self.project.model.create_poynting_flux_detector(**arguments)    


  # imports Constraints
  def import_constraint(self, obj):
    key = obj.get('key', 'NoneGiven')
    arguments = {
      'object': obj['object']
    }
    match obj['__name__']:
      case "PositionConstraint":
        arguments.update({
          'other_object': obj['other_object'],
          'axes': obj['axes']['__value__'],
          'object_positions': obj['object_positions']['__value__'],
          'other_object_positions': obj['other_object_positions']['__value__'],
          'margins': obj['margins']['__value__'],
          'grid_margins': obj['grid_margins']['__value__']
        })
        return [key,fdtdx.PositionConstraint(**arguments)]
      case "SizeConstraint":
        arguments.update({
          'other_object': obj['other_object'],
          'axes': obj['axes']['__value__'],
          'other_axes': obj['other_axes']['__value__'],
          'proportions': obj['proportions']['__value__'],
          'offsets': obj['offsets']['__value__'],
          'grid_offsets': obj['grid_offsets']['__value__']
        })
        return [key,fdtdx.SizeConstraint(**arguments)]
      case "SizeExtensionConstraint":
        arguments.update({
          'other_object': obj['other_object'],
          'axis': obj['axis'],
          'direction': obj['direction'],
          'other_position': obj['other_position'],
          'offset': obj['offset'],
          'grid_offset': obj['grid_offset']
        })
        return [key,fdtdx.SizeExtensionConstraint(**arguments)]
      case "GridCoordinateConstraint":
        arguments.update({
          'axes': obj['axes']['__value__'],
          'sides': obj['sides']['__value__'],
          'coordinates': obj['coordinates']['__value__'],
        })
        return [key,fdtdx.GridCoordinateConstraint(**arguments)]


  #iterates over every object in the JSON and calls the correct importer for each
  def import_objects(self, project_data: list[dict[str, Any]]):
    pml_imported = False
    # As we create new PMLs that willhave different names, we need to delete their existing constraints from the import
    delete_constraint = []

    constraints = []
    for item in project_data:
      type = item['__name__']
      match type:
        case 'UniformMaterialObject': self.import_UMO(item)
        case 'EnergyDetector' | 'FieldDetector' | 'ModeOverlapDetector' | 'PhasorDetector' | 'PoyntingFluxDetector':
          self.import_Detector(item)
        case 'ModePlaneSource' | 'GaussianPlaneSource': self.import_Source(item)
        case 'SizeConstraint' | 'PositionConstraint' | 'SizeExtensionConstraint' | 'GridCoordinateConstraint':
          if item['object'] not in delete_constraint:
            constraints.append(self.import_constraint(item))
        case 'PerfectlyMatchedLayer':
          delete_constraint.append(item['name'])

          # There is only one PML consisting of 6 sides (each side is an own object), but instead of importing 6 objects, we create a new PML here
          # (this is also why we need to delete existing constraints that refer to the old PML objects)
          if pml_imported == False:
            pml_imported = True
            self.project.model.create_pml_boundary_obj(item['partial_grid_shape']['__value__'][0])
    self.project.model.list_to_constraints(constraints)


  async def _extract_project_data(self, project_source: Any):
    """Extract project data from either uploaded file or already-decoded JSON."""
    if isinstance(project_source, list):
      return project_source
    if hasattr(project_source, 'read'):
      file_bytes = await project_source.read()
      return json.loads(file_bytes.decode('utf-8'))
    raise TypeError("Unsupported project input type for import")

  #gets the complete JSON as a dictionary, extracts the Simulation Config and Simulation Volume, calls the importer for all other objects
  async def import_from(self, project_source: Any):
    """Opens Project from existing File"""
    self.project.objects =[None]
    self.project.model = Model(self.project.objects)
    project_data = await self._extract_project_data(project_source)
    config = project_data[0]
    volume = project_data[1]

    self.project.model.create_simulation_volume(
      xyz= volume['partial_real_shape']['__value__'],
      material= self.project.model.material.get_material_from_settings(permittivity= volume['material']['permittivity'],
                                                                       permeability= volume['material']['permeability'],
                                                                       e_conductivity= volume['material']['electric_conductivity'],
                                                                       m_conductivity= volume['material']['magnetic_conductivity'],
                                                                       name= volume['material'].get('__name__', 'Unknown Material') )
      )

    self.import_objects(project_data)
    self.project.param.set_backend(config['backend'])
    self.project.param.set_time(config['time'])
    self.project.param.set_resolution(config['resolution'])
    self.project.param.set_courant_factor(config['courant_factor'])
    self.project.param.set_dtype(DType(config['dtype']['__dtype__']))  
  
  #reads in a Material List JSON and extracts the Materials into the list
  async def import_material_list(self, obj):
    for i in range(0, len(obj)):
      self.controller.model.material.create_new_material(obj[i]['permeability'], 
                                                         obj[i]['permittivity'], 
                                                         obj[i]['electric_conductivity'], 
                                                         obj[i]['magnetic_conductivity'], 
                                                         name = obj[i].get('__name__', 'Unknown Material') )