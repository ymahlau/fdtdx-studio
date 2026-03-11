from nicegui import events, ui
from fdtdx_studio.ui.ui_view import View
from fdtdx_studio.project.project import Project
import fdtdx

class Project_Dialog_Controller:
  """Controller for opening new and importing existing Projects"""
  def __init__(self, view: View, controller):
    self.view = view
    self.controller = controller

  async def new_scene_controller(self, project: Project | None = None):
    """handles the different Dialog Windows when opening or importing Projects"""
    if project is None:
      project = Project(controller= self.controller)
    def NoneCancel(): #Reached by not saving current Project
      """closes the Save Dialog and goes to the config panel for the new Project"""
      dialogSave.close()
      dialogSave.on('hide', on_dialog_closed)

    def SaveOpen(): #Reached by saving current Project
      """Closes the Save Dialog and goes to the SaveWhere Dialog"""
      dialogSave.close()
      dialogSave.on('hide', on_Save)
      
    def Saved(): #Reached after defining save Path
      """Closes the SaveWhere Dialog and goes to the config panel for the new project"""
      dialogSaveWhere.close()
      self.controller.open_Project(project)
      dialogSaveWhere.on('hide', on_dialog_closed)
      

    with ui.dialog() as dialogSave, ui.card(): #Asking if the current project should be saved
      ui.label('Would you like to save the current Project before progressing?')
      ui.button('Save').on_click(SaveOpen) 
      ui.button('Don\'t Save', on_click=lambda: self.controller.open_Project(project)).on_click(NoneCancel) 
      ui.button('Cancel', on_click=dialogSave.close)
    dialogSave.props('persistent')
    dialogSave.open()

    with ui.dialog() as dialogSaveWhere, ui.card(): #Defining Save Path
        def update_button():
          save.enabled = path.value
        ui.label('Where would you like the Project saved')
        def handle_name_change(e):
          if self.view.project is not None:
            self.view.project.set_name(e.value)
          update_button()
        
        def handle_save():
          if self.view.project is not None:
            self.view.project.save_Project()
        path = ui.input(label= 'Path', placeholder= 'Unnamed Project', on_change= handle_name_change)
        save = ui.button(text= 'Save', on_click= handle_save).on_click(Saved)
        ui.button(text= 'Cancel', on_click= dialogSaveWhere.close)
        update_button()

    def on_dialog_closed(): #New Config Panel for the new Project
      self.controller.ui_update()
      self.Config_Dialog()

    def on_Save(): #Saves the Project to current path. IF no Path, ask for Path
      if self.view.project is not None and self.view.project.name is not None:
        self.view.project.save_Project()
        self.controller.open_Project(project)
        on_dialog_closed()
      else:
        dialogSaveWhere.props('persistent')
        dialogSaveWhere.open()

    
  async def choose_Project(self):
    """Choose the Project the user wants to open"""
    json = None
    name = None

   
    #Next 2 Methods are needed for correctly displaying Dialog
    def pathed():
      dialogOpen.close()
      dialogOpen.on('hide', openDialogTree)

   
    async def handle_upload(e: events.UploadEventArguments):
      nonlocal json, name
      json = await e.file.json()
      name = e.file.name.replace('.json','')
      save.enable()
      

    async def openDialogTree():
      try:
        project = Project(Name=name,File=json,controller=self.controller)
        await self.new_scene_controller(project)
      except Exception as e:
        msg = "Invalid File: JSON-Format could not be read" if isinstance(e, KeyError) else repr(e)
        self.view.send_error(msg, 3000)
        
    with ui.dialog() as dialogOpen, ui.card(): #Dialog to choose Project
      ui.label('Which Project would you like to open')
      ui.upload(on_upload= handle_upload).props('accept=.json')
      save= ui.button(text= 'Save').on_click(pathed)
      ui.button(text= 'Cancel', on_click= dialogOpen.close)
    save.disable()
    dialogOpen.props('persistent')
    dialogOpen.open()

  # checks if given string is castable to float (maybe not nescessary anymore?)
  def isFloat(self, element: 'str') -> bool:
      """check if an input value is float"""
      try:
        float(element)
        return True
      except ValueError:
        return False    




  def Config_Dialog(self,first = False):
    #Dialogfenster für das Simulationsvolumen

    # loads last known state from browser localstorage
    async def LoadLast(dialog):
      imported =None
      imported = await self.controller.project.localproject_load()
      dialog.close()
      if(not imported):
        dialog.on('hide',actual_config_dialog)
      else:
        await self.controller.project.localmaterial_load()

    # config dialog for starting new project 
    def actual_config_dialog():
      assert self.view.left_drawer is not None
      assert self.view.right_drawer is not None
      self.view.left_drawer.Volume_Panel.Volume_panel()
      with ui.dialog() as dialogFirstConfig, ui.card():
        self.view.right_drawer.simparpanel.simulation_param_panel(dialogFirstConfig)
      dialogFirstConfig.props('persistent')
      dialogFirstConfig.open()

    def startNew(dialog):
      dialog.close()
      dialog.on('hide', actual_config_dialog)


    if first:
      #Dialog Window for choosing to load last state or beginning new project
      with ui.dialog() as loadLast, ui.card():
        ui.label("Do you want to load the last known state or do you want to start from scratch?")
        ui.button("Load last state", on_click= lambda: LoadLast(loadLast))
        ui.button("Start from scratch", on_click= lambda: startNew(loadLast))
      loadLast.props('persistent')
      loadLast.open()
      #dialogVolume.open()
    else:
      actual_config_dialog()

