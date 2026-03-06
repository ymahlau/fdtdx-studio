from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class MaterialObjectConfigPanel(AutoConfigPanel):
  """Creates the material object configuration panel UI."""
  
  def __init__(self, view, controller):
      """Initializes the MaterialObjectConfigPanel."""
      super().__init__(view, controller, 'UniformMaterialObject')