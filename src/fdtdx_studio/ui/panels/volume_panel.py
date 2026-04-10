import fdtdx 
import math
from nicegui import ui
from fdtdx_studio.ui.attribute_definitions import ALL_DOCS, ATTRIBUTE_TOOLTIP_FALLBACKS

def get_dyn_tooltip(attr: str, default: str) -> str:
    doc = ALL_DOCS.get('SimulationVolume', {}).get(attr)
    if doc: return doc
    doc = ATTRIBUTE_TOOLTIP_FALLBACKS.get(attr)
    if doc: return doc
    return default

class volume_panel():
  def __init__(self, *args):
    if len(args) == 2:
      self.drawer = args[0]
      self.controller = args[1]
    else:
      self.drawer = None
      self.controller = args[0]

  def volume_param_panel(self, dialog: ui.dialog = None):
    Volume: fdtdx.SimulationVolume = self.controller.project.objects[0]
    VTuple = Volume.partial_real_shape
    self.material = Volume.material


    with ui.card():
      ui.label("Simulation Volume").style('font-size: 18px; font-weight: bold;')
      
      with ui.row().classes('items-center gap-1'):
        ui.label('Size').style('font-size: 14px; padding-bottom: 0px; font-weight: bold;')
        ui.icon('info_outline').classes('text-grey-5 cursor-help').style('font-size: 14px;').tooltip(get_dyn_tooltip('partial_real_shape', "Sets the physical size of the simulation volume."))
      
      with ui.row().style('padding-top: 0px').classes('justify-center'):
        x = ui.number('Width', value=(VTuple[0]), step=0.000001, validation=self._validate).classes('w-1/6').tooltip('Width of the simulation volume (m)')
        y = ui.number('Height', value=(VTuple[1]), step=0.000001, validation=self._validate).classes('w-1/6').tooltip('Height of the simulation volume (m)')
        z = ui.number('Length', value=(VTuple[2]), step=0.000001, validation=self._validate).classes('w-1/6').tooltip('Length of the simulation volume (m)')
      
    def preset(W,H,L):
      nonlocal x,y,z
      x.value = W
      y.value = H
      z.value = L
      
    def preset_changed(val):
      if val == 'Small':
          preset(5e-6, 5e-6, 5e-6)
      elif val == 'Medium':
          preset(1e-5, 1e-5, 1e-5)
      elif val == 'Large':
          preset(1e-4, 1e-4, 1e-4)

    def get_preset_name(vt):
        if all(math.isclose(v, 5e-6, rel_tol=1e-5) for v in vt):
            return 'Small'
        if all(math.isclose(v, 1e-5, rel_tol=1e-5) for v in vt):
            return 'Medium'
        if all(math.isclose(v, 1e-4, rel_tol=1e-5) for v in vt):
            return 'Large'
        return None

    current_preset = get_preset_name(VTuple)
    ui.select(['Small', 'Medium', 'Large'], label='Preset Sizes', value=current_preset, on_change=lambda e: preset_changed(e.value)).classes('w-full')

    mat_names = [obj[0] for obj in self.controller.model.material.material_list]
    current_mat = self.controller.model.material.get_name_from_material(self.material)
    ui.select(mat_names, label='Material', value=current_mat, on_change=lambda e: self.choose_material_by_name(e.value)).classes('w-full')

    async def onSaved():
      self.controller.update_Simulation_Volume(x.value, y.value,z.value,self.material)
      self.controller.ui_update()
      if hasattr(self.drawer, 'update_vol_drawer'):
          await self.drawer.update_vol_drawer()
      if dialog is not None:
          dialog.close()

    self.save = ui.button("Apply", on_click=onSaved).classes('w-full')

  def _validate(self,value):
    try:
      if self.isFloat(value):
        if value > 0:
          self.save.enable()
          return None
        else:
          self.save.disable()
          return "Number must be greater than 0"
          
      else: 
        self.save.disable()
        return "Input must be a number"
    except (ValueError, TypeError):
      self.save.disable()
      return "Input must be a number"



  def choose_material_by_name(self, name):
    '''sets the material by its name'''
    for obj in self.controller.model.material.material_list:
        if obj[0] == name:
            self.material = obj[1]
            break

  def isFloat(self, element: 'str') -> bool:
      """check if an input value is float"""
      try:
        float(element)
        return True
      except ValueError:
        return False   