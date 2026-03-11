from nicegui import ui
from fdtdx_studio.parameter.DType import DType
import re

class simulation_parameters_panel():

  def __init__(self, drawer,  controller):
    self.drawer = drawer
    self.controller = controller
    
  def simulation_param_panel(self, dialog: ui.dialog | None = None):
     
      
      ui.label('Simulation Parameters').style('font-size: 18px; margin-bottom: 8px; font-weight: bold;')
      ui.select(['cpu', 'gpu', 'tpu', 'METAL'], label='Backend', value= self.controller.project.param.backend, on_change=lambda e: self.controller.project.param.set_backend(e.value)).classes('w-full ')
      # Use a text input for Time so scientific notation typing isn't interrupted by numeric parsing
      time = ui.input(label='Time', value=str(self.controller.project.param.time), validation=self._validate_Time).classes('w-full')
      res = ui.number(label='Resolution',value=self.controller.project.param.resolution, validation= self._validate)
      courant = ui.number(label='Courant Factor', value=self.controller.project.param.courant_factor,  validation= self._validate)
      ui.select({DType.Float_32: 'Float 32', DType.Float_64: 'Float 64'}, label='Data Type', value= self.controller.project.param.dtype, on_change=lambda e: self.controller.project.param.set_dtype(e.value)).classes('w-full ')
      
      async def on_save_clicked():
         await self.saveParams(time.value, res.value, courant.value)
         await self.drawer.update_drawer()

         if dialog is not None:
            dialog.close()
        
      self.button= ui.button('Apply', on_click= on_save_clicked)

  async def saveParams(self, time, res, courant):
    # `time` comes from a text input now; convert to float before saving
    try:
      t = float(time)
    except (ValueError, TypeError):
      t = self.controller.project.param.time
    self.controller.project.param.set_time(t)
    self.controller.project.param.set_resolution(float(res))
    self.controller.project.param.set_courant_factor(courant)
        
  def _validate_Time(self,value):
    # Accept complete floats (including scientific notation) and allow
    # partial inputs during typing (e.g. '80e-' or '1.2e') without
    # treating them as an error. Enable Apply only for complete > 0.
    try:
      if value is None:
        self.button.disable()
        return "Input must be a number"

      s = str(value).strip()
      if s == "":
        self.button.disable()
        return "Input must be a number"

      # Try to parse complete float first
      try:
        v = float(s)
        if v > 0:
          self.button.enable()
          return None
        else:
          self.button.disable()
          return "Number must be greater than 0"
      except (ValueError, TypeError):
        # Allow partial scientific notation while typing (no error shown)
        partial_pattern = r'^[\s]*[+-]?(?:\d+\.?\d*|\.?\d+)(?:[eE][+-]?\d*)?[\s]*$'
        if re.match(partial_pattern, s):
          self.button.disable()
          return None
        else:
          self.button.disable()
          return "Invalid number format"
    except Exception:
      self.button.disable()
      return "Input must be a number"
    
  def _validate(self, value):
    '''validates other inputs'''
    try:
      if self.isFloat(value):
        self.button.enable()
        return None
      else: 
        self.button.disable()
        return "Input must be a number"
    except (ValueError, TypeError):
      self.button.disable()
      return "Input must be a number"
  
  def isFloat(self, element: 'str') -> bool:
    """check if an input value is float"""
    try:
      float(element)
      return True
    except ValueError:
      return False     
        
  