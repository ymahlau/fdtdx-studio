from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class ModeSourcePanel(AutoConfigPanel):
  ''' Panel for configuring mode source parameters'''
  def __init__(self, view, controller):
    '''
    Initialize ModeSourcePanel instance.
    
    :param view: Reference to the View instance
    :param controller: Reference to the Controller instance
    '''
    super().__init__(view, controller, 'ModePlaneSource')