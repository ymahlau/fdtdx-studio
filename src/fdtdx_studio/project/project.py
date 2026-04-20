import asyncio

from nicegui import ui
from fdtdx_studio.parameter import simulation_parameters
from fdtdx_studio.json_handling.Export import Export
from fdtdx_studio.json_handling.Import import Import
from fdtdx_studio.parameter.datatypes.model import Model
import json


class Project:
  """Class for the Project. All Parameters and objects are gathered here to Save the Project in the end"""

  def __init__(self, controller, Name:str | None = None):
    """Initializes a new Project. If a Name is given, it opens the Project from an existing File"""
    self.projectstoragekey = "FDTDX_data"
    self.materialstoragekey = "FDTDX_material"
    self.exporter = Export(self)
    self.controller= controller
    self.importer = Import(self,controller)
    self.objects= [None]
    self.model = Model(self.objects)
    self.model.constraints.clear()
    #self.objects = self.model.track_object_list
    self.param = simulation_parameters.simulation_parameters()
    self.name: str | None= None

  @classmethod
  def create_new(cls, controller, Name: str | None = None):
    """Symchronously creates a new Project"""
    instance = cls(controller, Name)
    instance.model.create_simulation_volume()
    return instance

  @classmethod
  async def create_from_file(cls, controller, File: ui.upload.FileUpload, Name: str | None = None): 
    """Asynchronously creates a new Project from a given File"""
    instance = cls(controller, Name)
    if File is not None:
      await instance.importer.import_from(File)
    return instance

  def set_name(self, Name: str):
    """Set Project name to given value"""
    self.name = Name

  def save_Project(self):
    """Saves Project under Project Name. asks for name if none exists"""
    if self.name is not None:
      path = self.name.__add__('/data')
      self.exporter.export()
    else:
      self.save_Project_as()
  
  @staticmethod
  def update_button(button: ui.button, path: ui.input):
    button.enabled = path.value

    # interface for the user to choose the name of the file and where to save it
  def save_Project_as(self):
      """Sets the project name to input and then saves it"""
      with ui.dialog() as dialogSaveWhere, ui.card():
        def update_button():
          save.enabled = path.value
        ui.label('Where would you like the Scene saved')
        path = ui.input(label= 'Path', placeholder= 'Unnamed Project', on_change= lambda e: (self.set_name(e.value), update_button()))
        save = ui.button(text= 'Save', on_click= lambda: self.save_Project()).on_click(dialogSaveWhere.close)
        ui.button(text= 'Cancel', on_click= dialogSaveWhere.close)
        update_button()
      dialogSaveWhere.props('persistent')
      dialogSaveWhere.open()
  
  def _remove_null_types(self, obj):
        """
        Recursively traverses lists and dictionaries.
        Removes any object where the class name is 'Null'.
        """
        if isinstance(obj, dict):
            # Rebuild dict: keep items where value is NOT Null, and recurse into values
            return {
                k: self._remove_null_types(v) 
                for k, v in obj.items() 
                if type(v).__name__ != 'Null'
            }
        elif isinstance(obj, list):
            # Rebuild list: keep items that are NOT Null, and recurse into items
            return [
                self._remove_null_types(v) 
                for v in obj 
                if type(v).__name__ != 'Null'
            ]
        elif type(obj).__name__ == 'Null':
            # Handle edge case where the root object itself is Null
            return None 
        else:
            return obj
  
  # saves the current scene to the browser localstorage
  async def localproject_save(self):
        # 1. Get the raw data
        raw_data = self.exporter.build_export()
        
        # 2. Clean the data (Loop and delete Nulls)
        clean_data = self._remove_null_types(raw_data)

        # 3. Dump the clean data
        json_data = json.dumps(clean_data)
        
        await ui.run_javascript(
            f"""
            try {{
                localStorage.setItem('{self.projectstoragekey}', '{json_data}');
            }} catch (error) {{
                console.warn('Could not save to localStorage:', error);
            }}
            """,
            
        )
    
    # loads the last used scene from the browser localstorage
  async def localproject_load(self):
    importProject = None
    # reads the data from the localstorage with the name projectstoragekey
    importProject = await ui.run_javascript(
            f"""
            try {{
                const data = localStorage.getItem('{self.projectstoragekey}');
                return data ? JSON.parse(data) : {{}};
            }} catch (error) {{
                console.warn('Could not load from localStorage:', error);
                return {{}};
            }}
        """,
        )
    # checks if teh localstorage was empty
    if (len(importProject)>0):
        # tries to load the scene via the importer
      try:
        loaded_project = await Project.create_from_file(self.controller, File=importProject) 
        self.controller.open_Project(loaded_project)
        self.controller.ui_update()
        return True
        # if the import fails prints error messages and loads empty scene
      except:
        ui.notify("tried loading invalid config")
        print("tried loading invalid config")
        fallback_project = Project.create_new(self.controller)
        self.controller.open_Project(fallback_project)
        return False
        
    else:
      ui.notify("No previous state to load")
      return False
  

  # saves the list of custom materials from the browser localstorage
  async def localmaterial_save(self):
    json_data = json.dumps(self.exporter.build_material_list(self.model.material.get_material_list()))
    
    await ui.run_javascript(
            f"""
            try {{
                localStorage.setItem('{self.materialstoragekey}', '{json_data}');
            }} catch (error) {{
                console.warn('Could not save to localStorage:', error);
            }}
        """,
        )
  
  # loads the list of custom materials from the browser localstorage
  async def localmaterial_load(self):
    importMaterial = None
    importMaterial = await ui.run_javascript(
            f"""
            try {{
                const data = localStorage.getItem('{self.materialstoragekey}');
                return data ? JSON.parse(data) : {{}};
            }} catch (error) {{
                console.warn('Could not load from localStorage:', error);
                return {{}};
            }}
        """,
        )
    if (len(importMaterial)>0):
      try:
        await self.importer.import_material_list(importMaterial)
        self.controller.ui_update()
        return True
      except:
        ui.notify("tried loading invalid Material list")
        print("tried loading invalid Material list")
        return False
    else:
      ui.notify("No previous Material list to load")
      return False

