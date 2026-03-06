from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class PhasorDetectorPanel(AutoConfigPanel):
  '''UI for the phasor detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller, 'PhasorDetector')