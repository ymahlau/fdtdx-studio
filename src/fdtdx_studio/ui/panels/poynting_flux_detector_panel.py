from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

#Version 1.1
class PoyntingFluxDetectorPanel(AutoConfigPanel):
  '''UI for the poynting flux detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller, 'PoyntingFluxDetector')