from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class EnergyDetectorPanel(AutoConfigPanel):
  '''UI for the energy detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller, 'EnergyDetector')
