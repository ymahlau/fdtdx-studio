from nicegui import ui
from fdtdx_studio.ui.scene_3d.main_section import MainSection
from fdtdx_studio.ui.panels.material_object_config_panel import MaterialObjectConfigPanel as MaterialObjectConfigurationPanel
from fdtdx_studio.ui.panels.detector_panel import DetectorConfigurationPanel
from fdtdx_studio.project.project import Project
from fdtdx_studio.project.project_dialog_controller import Project_Dialog_Controller
from fdtdx_studio.ui.ui_elements.left_drawer import LeftDrawer
from fdtdx_studio.ui.ui_elements.right_drawer import RightDrawer



class View:
  """Main UI view class containing the 3D scene and UI components."""

  
  def __init__(self):
    """Initialize the main UI view with color theme, scene, objects, and UI containers."""
    ui.colors(primary = '#624182', secondary = '#E3E3E3', accent= '#F3E155') # Set global UI colors, button colors are dictated by primary color
    
    #Scene where all items and parameters should be saved to simplify exporting and importing
    self.project = None
    self.dialog_controller = None
    self.row_list =[]
    self.scrollarea_sim_objects = None
    self.config_panel = None
    
    # Config panel instances, to be rendered into self.config_panel (owns its own widgets)
    self.objects_panel = None
    self.detector_panel = None
    self.left_drawer = None

  def build_base_ui(self, controller):  
    """Build the base UI structure including header, main section, and drawers."""     
    # Header
    self.build_header()

   
    # Main View Area with 3D Scene and Center View Button
    self.main_section = MainSection(controller)

    # Left Drawer for Lists of Simulation Objects, Sources, Detectors, Materials each with scrollable Expansion Panels
    self.left_drawer = LeftDrawer(self, controller)
  
    # Right Drawer for Configuration
    self.right_drawer = RightDrawer(self, controller)

    # Configuration Panels
    self.objects_panel = MaterialObjectConfigurationPanel(self, controller)
    self.detector_panel = DetectorConfigurationPanel(self, controller)

    #open first Project config Dialog
    self.dialog_controller.Config_Dialog(True)
    
  def open_Project(self, Project: Project, controller):
    '''
    Reset the UI to load the given Project, updating the left drawer and initializing the dialog controller.
    
    :param Project: New Project to load into the UI.
    :type Project: Project
    :param controller: main controller instance
    :type controller: Controller
    '''

    if self.left_drawer is not None:
      self.left_drawer.clear_drawer()
    self.project = Project
    self.dialog_controller = Project_Dialog_Controller(self, controller)
    ui.notify('Project opened')
  
  def build_header(self):
    '''
    Build the header section of the UI with logo, title, and action buttons (Help, New Scene, Export, Import).  
    '''
    with ui.header().style('background-color: #17032B').classes('items-center justify-between').style('padding: 0px;') as self.header:
      with ui.row().classes('items-center').style('margin-left: 8px;'):
        ui.image("fdtdx_studio/fdtdx.svg").style('height: 24px; width: 24px; margin-left: 16px;')
        ui.label('FDTDX Studio').style('color: #BE44E4; font-size: 24px; margin-left: 0px; font-weight: bold; align-self: center;')
      with ui.row().classes('items-center justify-end').style('margin-right: 4px;'):
        ui.button(icon= 'help', color = None).props('flat').style('padding: 0px; color:#F3E155;').on_click(lambda: ui.navigate.to('https://fdtdx.readthedocs.io/en/latest/', new_tab= True)) 
        ui.separator().props('vertical').style('background-color: #DDA091; width: 2px; height: 28px; padding: 0px; margin: 0px 8px; align-self: center;')
        ui.button(on_click=lambda: self.dialog_controller.new_scene_controller(), icon= 'add_box', color= None).props('flat').style('padding: 0px; color: #CF78B4;').tooltip('New Project')
        ui.button(on_click=lambda: self.dialog_controller.choose_Project(), icon = 'file_upload', color = None).props('flat').style('padding: 0px; color: #BE44E4;').tooltip('Import')
        with ui.button(icon='file_download', color = None).props('flat').style('padding: 0px; margin-right: 16px; color: #BE44E4;').tooltip('Export'):
          with ui.menu() as menu:
            ui.menu_item('Save Project', lambda: self.project.save_Project(), auto_close= False)
            ui.menu_item('Save Project as', lambda: self.project.save_Project_as(), auto_close= False)
            ui.menu_item('Close', on_click= menu.close)
  
  def send_error(self, message, timeout=10000):
    """
    Display an error notification in the UI.
    :param message: The error message to display.
    :type message: str
    :param timeout: Duration in milliseconds before the notification disappears. Default is 10000 ms.
    :type timeout: int
    """
    ui.notify(message=message,close_button=True, type='warning', timeout=timeout)


  def load_config_panel(self, type_panel):
    """Render the given configuration panel into the right drawer."""
    if self.config_panel and type_panel:
      type_panel.render_into(self.config_panel)

  