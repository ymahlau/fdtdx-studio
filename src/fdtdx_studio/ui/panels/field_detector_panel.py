from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class FieldDetectorPanel(AutoConfigPanel):
  '''UI for the field_detector_panel'''
  def __init__(self, view, controller):
    super().__init__(view, controller, 'FieldDetector')
