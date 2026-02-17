from fdtdx_studio.ui.panels.auto_config_panel import AutoConfigPanel

class GaussianSourcePanel(AutoConfigPanel):
  '''Generates UI Configuration of Parameters specific to the Gaussian Plane Source'''

  def __init__(self, view, controller):
        '''
        Initialize GaussianSourcePanel instance.
        
        :param view: Reference to the View instance
        :param controller: Reference to the Controller instance
        '''
        
        super().__init__(view, controller, 'GaussianPlaneSource')