from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class ModeOverlapDetectorPanel(AutoConfigPanel):
  '''UI for the mode overlap detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller, 'ModeOverlapDetector')