import fdtdx 
from nicegui import ui
from fdtdx_studio.ui.attribute_definitions import ALL_DOCS, ATTRIBUTE_TOOLTIP_FALLBACKS

def get_dyn_tooltip(attr: str, default: str) -> str:
    doc = ALL_DOCS.get('SimulationVolume', {}).get(attr)
    if doc: return doc
    doc = ATTRIBUTE_TOOLTIP_FALLBACKS.get(attr)
    if doc: return doc
    return default

class volume_panel():
  def __init__(self, controller):
    self.controller = controller

  def Volume_panel(self):
    Volume: fdtdx.SimulationVolume = self.controller.project.objects[0]
    VTuple = Volume.partial_real_shape
    self.material = Volume.material


    with ui.dialog() as dialogVolume, ui.card():
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
        
      with ui.row().classes('items-center gap-1'):
        ui.label("Preset Sizes:").style('font-weight: bold;')
        ui.icon('info_outline').classes('text-grey-5 cursor-help').style('font-size: 14px;').tooltip("Quickly set the volume dimensions to common predefined sizes.")
      with ui.row():
        ui.button("Small", on_click= lambda: preset(5e-6,5e-6,5e-6)).tooltip('Sets size to 5µm x 5µm x 5µm')
        ui.button("Medium",on_click= lambda: preset(1e-5,1e-5,1e-5)).tooltip('Sets size to 10µm x 10µm x 10µm')
        ui.button("Large", on_click= lambda: preset(1e-4,1e-4,1e-4)).tooltip('Sets size to 100µm x 100µm x 100µm')

      with ui.row().classes('items-center gap-1'):
        ui.label("Material:").style('font-weight: bold;')
        ui.icon('info_outline').classes('text-grey-5 cursor-help').style('font-size: 14px;').tooltip(get_dyn_tooltip('material', "Sets the background material of the simulation volume."))
      with ui.dropdown_button(self.controller.model.material.get_name_from_material(self.material)).classes('w-1/3') as self.material_show:
          for obj in self.controller.model.material.material_list:
            ui.item(text=obj[0], on_click= lambda material=obj: self.choose_material(material))

      def onSaved():
        dialogVolume.close()
        self.controller.update_Simulation_Volume(x.value, y.value,z.value,self.material)
        self.controller.ui_update()

      self.save= ui.button("Save and Close").on_click(onSaved)

    dialogVolume.props('persistent')
    dialogVolume.open()

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



  def choose_material(self, obj):
    '''sets the material and updates the ui accordingly'''
    self.material = obj[1]
    self.material_show.close()
    self.material_show.text = obj[0]

  def isFloat(self, element: 'str') -> bool:
      """check if an input value is float"""
      try:
        float(element)
        return True
      except ValueError:
        return False   