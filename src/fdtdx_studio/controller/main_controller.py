from fdtdx_studio.ui.ui_view import View
import inspect
from fdtdx_studio.parameter.datatypes.model import Model
import fdtdx
from nicegui import ui, events
from fdtdx_studio.project.project import Project
from fdtdx_studio.ui.panels import ObjectConfigPanel, GaussianSourcePanel, ModeSourcePanel, MaterialObjectConfigPanel, FieldDetectorPanel, PoyntingFluxDetectorPanel, EnergyDetectorPanel, ModeOverlapDetectorPanel, Material_panel
import json
import inspect

class Controller:
  """Main controller class that mediates between the View and Model."""

  def __init__(self):
    """Initialize the Controller with references to the View and Model."""
    
    self.view = View()
    self.open_Project(Project(controller=self))
    # Build the UI here so view.scene and other widgets are created
    self.view.build_base_ui(self)
    self.type_panel: ObjectConfigPanel


  def open_Project(self, Project: Project):
    '''initialize the project, set the local model variable correctly, open the project in the ui'''
    self.project = Project
    self.model = self.project.model
    self.view.open_Project(Project, self)

  def add_object(self, popup=None, name='jeff', length=1, width=1, height=1, color='Red',typ=None, verbose = False, material = fdtdx.Material()):
    '''create model entry for a Uniform Material Object'''
    partial_real_shape = (length, width, height)
    partial_real_position = (0, 0, 0)
    if verbose:
      print(f"Adding object to model: name={name}, partial_real_shape={partial_real_shape}, partial_real_position={partial_real_position}, color={color}\n")
    name = self.model.namecheck(name) #checks if the name is unique and changes it if not
    self.model.create_material_obj(name=name, partial_real_shape=partial_real_shape, partial_real_position=partial_real_position, color=color, material= material)
    self.view.left_drawer.scrollarea_add_Object((name,typ))
    self.view.main_section.add_object((name, typ, partial_real_shape, partial_real_position, color))
    #close popup after reset of inputs
    popup.close_self()

  def set_pml_thickness(self, thickness):
    '''sets PML thickness to the given value'''
    if thickness is None:
      thickness = 0
    self.model.create_pml_boundary_obj(thickness=thickness)

  def choose_box(self, name):
    """Select an object by name and update the config panel."""
    self.model.config(name)
    # Loads the UI-config panel for configuring the selected object by the user
    self.choose_config_panel()
    # makes everthing except the choosen object transparent
    self.view.main_section.highlight(name)

  
  def choose_config_panel(self):
    """Choose the appropriate configuration panel based on the current object type and load it."""
    match self.model.get_current_type():
      case 'GaussianPlaneSource':
        self.type_panel = GaussianSourcePanel(self.view, self)
      case 'ModePlaneSource':
        self.type_panel = ModeSourcePanel(self.view, self)
      case 'UniformMaterialObject':
        self.type_panel = MaterialObjectConfigPanel(self.view, self)
      case 'FieldDetector':
        self.type_panel = FieldDetectorPanel(self.view, self)
      case 'PoyntingFluxDetector':
        self.type_panel = PoyntingFluxDetectorPanel(self.view, self)
      case 'EnergyDetector':
        self.type_panel = EnergyDetectorPanel(self.view, self)
      case 'ModeOverlapDetector':
        self.type_panel = ModeOverlapDetectorPanel(self.view, self)
    
    self.view.load_config_panel(self.type_panel)
    self.update_config_objects()

  def add_gaussian_source(self, project = None, popup=None, typ=None, name=None, partial_real_shape=None, partial_real_position = (0.0,0.0,0.0), color=None, 
                          direction=None, wave=None, azimuth_angle=None, elevation_angle=None, 
                          temporal_profile=None, switch=None, fixed_E_polarization_vector=None, 
                          fixed_H_polarization_vector=None, normalize_by_energy=None, std=None, radius=None):
    '''adds new gaussian source to the model list'''
    
    if wave : wave_character=fdtdx.WaveCharacter(**wave)
    if switch: switch = fdtdx.OnOffSwitch(**switch)
    temporal_profile_type = temporal_profile.pop("type") if temporal_profile else None
    if temporal_profile and temporal_profile_type == "GaussianPulseProfile":
      temporal_profile = fdtdx.GaussianPulseProfile(**temporal_profile)
    elif temporal_profile and temporal_profile_type == "SingleFrequencyProfile":
      temporal_profile = fdtdx.SingleFrequencyProfile(**temporal_profile)
    keys = list(inspect.signature(self.model.create_gaussian_plane_source_obj).parameters.keys())
    kwargs = {k: locals()[k] for k in keys if k in locals()}
    
    if 'name' in kwargs and project is None:
      kwargs['name'] = self.model.namecheck(kwargs['name']) #checks if the name is unique and changes it if not
    if project:
      project.model.create_gaussian_plane_source_obj(**kwargs)
    else:
      self.model.create_gaussian_plane_source_obj(**kwargs)
      self.view.left_drawer.scrollarea_add_Object((kwargs['name'],typ))
    #TODO they are just boxes for now
      self.view.main_section.add_object((name, typ, partial_real_shape, (0,0,0), color))     



  def add_mode_source(self, project=None, popup=None, typ=None, name=None, partial_real_shape=None, partial_real_position=(0.0,0.0,0.0), color=None, 
                          direction=None, wave=None, azimuth_angle=None, elevation_angle=None, 
                          temporal_profile = None, switch=None, filter_pol=None, mode_index=None):
    '''adds new mode source to the model list'''
    if wave : wave_character=fdtdx.WaveCharacter(**wave)
    if switch: switch = fdtdx.OnOffSwitch(**switch)
    temporal_profile_type = temporal_profile.pop("type") if temporal_profile else None
    if temporal_profile and temporal_profile_type == "GaussianPulseProfile":
      temporal_profile = fdtdx.GaussianPulseProfile(**temporal_profile)
    elif temporal_profile and temporal_profile_type == "SingleFrequencyProfile":
      temporal_profile = fdtdx.SingleFrequencyProfile(**temporal_profile)
    
    keys = list(inspect.signature(self.model.create_mode_plane_source_obj).parameters.keys())
    # todo: Capture locals outside: Python 3 dict comprehensions have an isolated local scope.
    local_snapshot = locals()
    kwargs = {k: local_snapshot[k] for k in keys if k in local_snapshot}
    if 'name' in kwargs and project is None:
      kwargs['name'] = self.model.namecheck(kwargs['name']) #checks if the name is unique and changes it if not
    if project:
      project.model.create_mode_plane_source_obj(**kwargs)
    else:
      self.model.create_mode_plane_source_obj(**kwargs)
      self.view.left_drawer.scrollarea_add_Object((kwargs['name'],typ))
    #TODO they are just boxes for now
      self.view.main_section.add_object((name, typ, partial_real_shape, (0,0,0), color))     



    
  def update_Simulation_Volume(self, x: float = 1, y: float = 1, z: float =1, material = None):
    '''updates the simulation values with the given values'''
    #Deletes old Simulation Volume if needed:
    if len(self.view.main_section.objects) > 0:
      self.view.main_section.delete_object('Simulation_Volume')
    self.model.update_simulation_volume(x, y, z, material)
    self.view.main_section.add_simulation_volume((None,None,[x,y,z]))

  def update_config_objects(self):
    """Update all config panel widgets with current object's data from model."""
    self.type_panel.update_values(self.model.get_current_parameters())
   

  def get_current_object(self):
    """Get the index of the currently selected object from the model."""
    return self.model.current
  

  # Object Save Function

  def saveParams(self, parameters):
    """Save OBJECT parameters from the config panel to the model and update the UI."""
    self.model.create_material_obj(**parameters , index=self.model.current)
    self.ui_update()

  # Source Save Functions

  def saveGaussianPlaneSourceParams(self, parameters):
    """Save GAUSSIAN SOURCE parameters from the config panel to the model and update the UI."""
    if "wave_character" in parameters : parameters["wave_character"]=fdtdx.WaveCharacter(**parameters["wave_character"])
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    if "temporal_profile" in parameters:
      temp_profile = parameters["temporal_profile"]
      temp_profile_type = temp_profile.pop("type")
      if temp_profile_type == "GaussianPulseProfile":
        parameters["temporal_profile"] = fdtdx.GaussianPulseProfile(**temp_profile)
      elif temp_profile_type == "SingleFrequencyProfile":
        parameters["temporal_profile"] = fdtdx.SingleFrequencyProfile(**temp_profile)
      else:
        raise ValueError(f"Unknown temporal profile type: {temp_profile_type}")
      
    self.model.create_gaussian_plane_source_obj(**parameters , index=self.model.current)
    self.ui_update()

  def saveModePlaneSourceParams(self, parameters):
    """Save MODE SOURCE parameters from the config panel to the model and update the UI."""
    if "wave_character" in parameters : parameters["wave_character"]=fdtdx.WaveCharacter(**parameters["wave_character"])
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    if "temporal_profile" in parameters:
      temp_profile = parameters["temporal_profile"]
      temp_profile_type = temp_profile.pop("type")
      if temp_profile_type == "GaussianPulseProfile":
        parameters["temporal_profile"] = fdtdx.GaussianPulseProfile(**temp_profile)
      elif temp_profile_type == "SingleFrequencyProfile":
        parameters["temporal_profile"] = fdtdx.SingleFrequencyProfile(**temp_profile)
      else:
        raise ValueError(f"Unknown temporal profile type: {temp_profile_type}")
    self.model.create_mode_plane_source_obj(**parameters , index=self.model.current)
    self.ui_update()


  # Detector Save Functions. Not all are used but if eventually implemented it should be usefull uwu~

  def savePoyntingFluxDetectorParams(self, parameters):
    """Save POYNTING FLUX DETECTOR parameters from the config panel to the model and update the UI."""
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    self.model.create_poynting_flux_detector(**parameters , index=self.model.current)
    self.ui_update()

  def saveModeOverlapDetectorParams(self, parameters):
    """Save MODE OVERLAP DETECTOR parameters from the config panel to the model and update the UI."""
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    if "wave_character" in parameters : parameters["wave_character"]=fdtdx.WaveCharacter(**parameters["wave_character"])
    self.model.create_mode_overlap_detector(**parameters , index=self.model.current)
    self.ui_update()
  
  def savePhasorDetectorParams(self, parameters):
    """Save PHASOR DETECTOR parameters from the config panel to the model and update the UI."""
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    if "wave_character" in parameters : parameters["wave_character"]=fdtdx.WaveCharacter(**parameters["wave_character"])
    self.model.create_phasor_detector(**parameters , index=self.model.current)
    self.ui_update()
  
  def saveFieldDetectorParams(self, parameters):
    """Save FIELD DETECTOR parameters from the config panel to the model and update the UI."""
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    self.model.create_field_detector_obj(**parameters , index=self.model.current)
    self.ui_update()

  def saveEnergyDetectorParams(self, parameters):
    """Save ENERGY DETECTOR parameters from the config panel to the model and update the UI."""
    if "switch" in parameters: parameters["switch"] = fdtdx.OnOffSwitch(**parameters["switch"])
    self.model.create_energy_detector_obj(**parameters , index=self.model.current)
    self.ui_update()
    
  def delete_object(self, name):
    '''deletes an object by name from the scene'''
    self.model.config(name)
    self.model.delete_by_object_name(name)
    
    self.ui_update()
  
  def view_material(self, obj):
    '''opens material config panel in right drawer'''
    panel= Material_panel(self.view, self)
    panel.getMaterial(obj)
    self.view.load_config_panel(panel)

  
  def add_material(self, Permittivity, Permeability, Electrical_conductivity, Magnetic_conductivity, name):
    '''adds custom material to current scene'''
    name = self.namecheck_material(self.model.material.get_material_list(), name)
    self.model.material.create_new_material(permittivity=Permittivity, permability=Permeability, e_conductivity=Electrical_conductivity, m_conductivity=Magnetic_conductivity, name=name)
    self.view.left_drawer.update_materials()

  def update_material(self, obj, index):
    '''updates the material list with obj(the material) '''
    self.model.material.material_list.pop(index)
    obj[0] = self.namecheck_material(self.model.material.get_material_list(),obj[0])
    self.model.material.material_list.insert(index,obj)
    self.view.left_drawer.update_materials()
    ui.timer(0, lambda: self.project.localmaterial_save(), once=True)
    
    

  def download_material_list(self):
    '''exports material list'''
    self.project.exporter.export_material_list(self.model.material.material_list)

  async def upload_material_list(self):
    '''reads material list JSON and builds the custom material list from it'''
    json = None
    #Next 2 Methods are needed for correctly displaying Dialog
    async def pathed():
      dialogOpen.close()
      print(json)
      await self.project.importer.import_material_list(json,self)
      self.view.left_drawer.update_materials()

    async def handle_upload(e: events.UploadEventArguments):
      nonlocal json
      json = await e.file.json()
      if json[0]['__module__'] == "fdtdx.materials":
        save.enable()
      else:
        denied.set_visibility(True)
    
    with ui.dialog() as dialogOpen, ui.card(): #Dialog to choose Material List
      ui.label('Import custom Material List')
      ui.upload(on_upload= handle_upload).props('accept=.json')
      denied = ui.label("The File is not a valid material list and/or empty").style('color: red')
      save= ui.button(text= 'Save').on_click(pathed)
      ui.button(text= 'Cancel', on_click= dialogOpen.close)
    save.disable()
    denied.set_visibility(False)
    dialogOpen.props('persistent')
    dialogOpen.open()

    
  def ui_parse_objectlist_scrollarea(self):
    s = self.project.param
    con = {'time':s.time, 'resolution':s.resolution, 'backend':s.backend, 'dtype':s.dtype, 'courant_factor':s.courant_factor, 'gradient_config':s.gradient_config}
    dims = self.model.get_all_dimensions(config=con)

    return_list = []

    for i in self.model.get_track_object_list():
      if isinstance(i, fdtdx.PerfectlyMatchedLayer):
        return_list.append((i.partial_grid_shape[0], i.__class__.__name__))
      else:
        return_list.append((i.name, i.__class__.__name__, dims[i.name][0], dims[i.name][1], i.color))
    return return_list

  def namecheck_material(self,list, name, index = 1):
      '''namechecks materials to prevent materials with the same name, and auto incerements if same name already exists'''
      for obj in list:
        if obj[0] == name:
          if obj[2] == False:
            name = 'Custom ' + name
          else:
            if name[-2] == str(index -1) and name[-1] == ')':
              name = name[:-3]
            name = name.__add__('('+str(index)+')')
            index += 1
          self.namecheck_material(list, name, index= index)
      return name

  # UI Update to be called if backend variables are changed
  def ui_update(self):
    '''called when any relevant variable is updated, updates entire ui accordingly, saves projects to browser localstorage'''
    try:
      ui_objects = self.ui_parse_objectlist_scrollarea()
      self.view.main_section.update(ui_objects)
    except Exception as e:
      self.view.send_error(f"Conflicting constraints for {str(e)}")
      #should still update left draw with name changes etc cause it does still get saved 
      ui_objects = []
      for i in self.model.get_track_object_list():
        if i.__class__.__name__ == "PerfectlyMatchedLayer":
          ui_objects.append((i.partial_grid_shape[0], i.__class__.__name__))
        else:
          ui_objects.append((i.name, i.__class__.__name__, i.color))
      self.view.main_section.update(ui_objects[:1])
    self.view.left_drawer.update(ui_objects[1:])
    
    #ui.timer(0, lambda: self.view.right_drawer.update_drawer(), once=True)
    #The above line will not work at this moment. It should be used to clear the right panel after making changes. 
    # If its called from a popup or a panel which is deleting itself it throws an error because the parent vanishes 
    # while ui_update is running, breaking it.
    
    ui.timer(0, lambda: self.project.localproject_save(), once=True)


  def save_constraints(self, object_name, cons):
    #delete removed constraints
    old = [c['key'] for c in self.model.get_obj_constraints(object_name)]
    new = [c["key"] for c in cons]
    delete = [k for k in old if k not in new]
    for key in delete: self.model.delete_constraint(key)
    for con in cons:
      match(con["type"]):
        case "PositionConstraint":
          self.model.add_pos_con(object_name, con['other_object'], con['axes'], con['object_positions'], con['other_object_positions'], con['margins'], con['grid_margins'], con['key'])
        case "SizeConstraint":
          self.model.add_size_con(object_name, con['other_object'], con['axes'], con['other_axes'], con['proportions'], con['offsets'], con['grid_offset'], con['key'])
        case "SizeExtensionConstraint":
          self.model.add_size_ex_con(object_name, con['other_object'], con['axis'], con['direction'], con['other_position'], con['offset'], con['grid_offset'], con['key'])
        case "GridCoordinateConstraint":
          self.model.add_grid_con(object_name, con['axes'], con['sides'], con['coordinates'], con['key'])    
    



#======= DETECTOR STUFF =============================================================================================
  def add_new_detector(self, *, detector_type: str, popup, typ: str, **kwargs):
  
    """
    Central dispatcher for ALL detector creation.

    Called ONLY from BaseDetectorPopup._call_add().
    """

  # ----------------------------
  # 1. Dispatch table
  # ----------------------------
    detector_factories = {
        'FIELD': self.model.create_field_detector_obj,
        'ENERGY': self.model.create_energy_detector_obj,
        'POYNTING': self.model.create_poynting_flux_detector,
        'MODE_OVERLAP': self.model.create_mode_overlap_detector,
        'PHASOR': self.model.create_phasor_detector,
    }

    if detector_type not in detector_factories:
      raise ValueError(f'Unknown detector type: {detector_type}')
    


    create_fn = detector_factories[detector_type]

    # ----------------------------
    # 2. Create detector in MODEL
    # ----------------------------

    sig = inspect.signature(create_fn)
    filtered_kwargs = {
        k: v for k, v in kwargs.items()
        if k in sig.parameters
    }
    if 'name' in filtered_kwargs:
      filtered_kwargs['name'] = self.model.namecheck(filtered_kwargs['name']) #checks if the name is unique and changes it if not
    
    if ('partial_real_shape' in sig.parameters and all(k in kwargs for k in ('length', 'width', 'height'))):
      
      filtered_kwargs['partial_real_shape'] = (

        kwargs['length'],
        kwargs['width'],
        kwargs['height'],
    )
      
    detector_obj = create_fn(**filtered_kwargs)

    # ----------------------------
    # 3. Update UI (Drawer + Scene)
    # ----------------------------
    name = detector_obj.name
    obj_type = detector_obj.__class__.__name__
    shape = getattr(detector_obj, 'partial_real_shape', None)
    pos = getattr(detector_obj, 'partial_real_position', (0, 0, 0))
    if pos is None or any(p is None for p in pos):
      pos = (0, 0, 0)

    color = getattr(detector_obj, 'color', None)

    self.view.left_drawer.scrollarea_add_Object((name, f"{detector_obj.__class__.__name__}"))

    self.view.main_section.add_object((name, obj_type, shape, pos, color))

    # ----------------------------
    # 4. Reset popup & close dialog
    # ----------------------------
    popup.close_self()

    return detector_obj
