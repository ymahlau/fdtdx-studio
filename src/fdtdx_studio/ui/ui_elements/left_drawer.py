from nicegui import ui
from fdtdx_studio.ui.popups.pop_up_new_object import pop_up_new_object
from fdtdx_studio.ui.popups.pop_up_new_source import pop_up_new_source
import fdtdx
from fdtdx_studio.ui.popups.detector_popup import DetectorPopup
from fdtdx_studio.ui.panels.volume_panel import volume_panel
from fdtdx_studio.ui.popups.pop_up_new_material import pop_up_new_material
from fdtdx.objects.static_material.static import UniformMaterialObject, SimulationVolume

class LeftDrawer:
    """Creates the left drawer UI visible on the main view, used for creating and managing simulation components.
    
    Contains expansion panels for Simulation Objects, Sources, Detectors, and Materials.
    """

    def __init__(self, view, controller):
        """Initializes the LeftDrawer with references to the main view and controller."""
        self.controller = controller
        self.view = view
        # LeftDrawer manages its own popup + scrollarea
        self.detector_popup = DetectorPopup(controller)
        self.Volume_Panel = volume_panel(controller)
        self.scrollarea_sim_objects = None
        self.scrollarea_source_objects = None
        self.scrollarea_sim_detector = None
        self.pml_thickness = None
        self.build()

    def build(self):
        """Builds the left drawer UI components."""
        with ui.left_drawer(elevated=True).style('background-color: #E3E3E3').classes('justify-start') as self.left_drawer:    
          # Expansion for Simulation Objects
          with ui.expansion().props('open').classes('w-full') as self.sim_obj_exp:
            with self.sim_obj_exp.add_slot('header'):
              with ui.row().classes('w-full items-center justify-between'):
                ui.label('Simulation Volume').style('font-size: 15px')
            with ui.scroll_area().classes('w-full h-48 ml-4') as self.scrollarea_sim_volume:
              ui.button("Simulation Volume", on_click= lambda: self.Volume_Panel.Volume_panel())
              

          with ui.expansion().props('open').classes('w-full') as self.sim_obj_exp:
            with self.sim_obj_exp.add_slot('header'):
              with ui.row().classes('w-full items-center justify-between'):
                ui.label('Simulation Objects').style('font-size: 15px')
                ui.button(icon='add', color = None, on_click=lambda: pop_up_new_object(self.controller).open_new_object_popup()).props('flat').style('pointer-events: auto; z-index: 10')
                      
            with ui.scroll_area().classes('w-full h-48 ml-4') as self.scrollarea_sim_objects:
              pass

          # Expansion for Sources    
          with ui.expansion().props('open').classes('w-full') as self.source_exp:
            with self.source_exp.add_slot('header'):
              with ui.row().classes('w-full items-center justify-between'):
                  ui.label('Sources').style('font-size: 15px')
                  ui.button('', icon='add', color = None, on_click=lambda: pop_up_new_source(self.controller).open_new_source_popup()).props('flat')
            with ui.scroll_area().classes('w-full h-48 ml-4') as self.scrollarea_source_objects: 
              pass

          #Expansion for Detectors
          with ui.expansion().props('open').classes('w-full') as detector_exp:
            with detector_exp.add_slot('header'):
              with ui.row().classes('w-full items-center justify-between'):
                  ui.label('Detectors').style('font-size: 15px')
                  ui.button(icon='add', color = None, on_click=self.detector_popup.open).props('flat').style('pointer-events: auto; z-index: 10')
                      
            with ui.scroll_area().classes('w-full h-48 ml-4') as self.scrollarea_sim_detector:
              pass

          ui.separator().style('margin: 8px 0;')

          with ui.row().classes('w-full items-center justify-between'):
            ui.label('PML-Thickness:').style('font-size: 15px').classes('flex-1').props('dense')
            self.pml_thickness = ui.number(value=0, min=0, on_change=lambda e: self.controller.set_pml_thickness(e.value)).classes('flex-1')

          # Expansion for Materials
          with ui.expansion().props('open').classes('w-full') as material_exp:
            with material_exp.add_slot('header'):
              with ui.row().classes('w-full items-center justify-between'):
                ui.label('Materials').style('font-size: 15px').classes('flex-1').props('dense')
                ui.button(icon='file_upload',color= None, on_click= lambda: self.controller.upload_material_list()).props('flat dense size=sm').tooltip('Upload a List of custom materials')
                ui.button(icon='file_download',color=None, on_click= lambda: self.controller.download_material_list()).props('flat dense size=sm').tooltip('Download your custom Materials. This List will not contain Preset Materials')
                ui.button(icon='add', on_click= lambda: pop_up_new_material(self.controller).open_new_material_popup(), color = None).props('flat dense').tooltip('Add new material')

            with ui.scroll_area().classes('w-full h-48 ml-4') as self.scrollarea_materials:
              self.update_materials()
                      
    
    def clear_drawer(self):
      '''clears all scrollareas in left drawer'''
      assert self.scrollarea_sim_detector is not None
      assert self.scrollarea_sim_objects is not None
      assert self.scrollarea_source_objects is not None
      self.scrollarea_sim_detector.clear()
      self.scrollarea_sim_objects.clear()
      self.scrollarea_source_objects.clear()
       
    def scrollarea_add_Object(self, object):
      '''
      create UI row in scroll area (safe)
      param object: tuple with (name, type)
      type object: tuple
      '''
      match object[1]:
        case "UniformMaterialObject" | 'scrollarea_sim_objects':
          container = self.scrollarea_sim_objects
        case "ModePlaneSource" | "GaussianPlaneSource" | 'scrollarea_sim_sources':
          container = self.scrollarea_source_objects
        case "EnergyDetector" | "FieldDetector" | "ModeOverlapDetector" | "PhasorDetector" | "PoyntingFluxDetector" | 'scrollarea_sim_detector':
          container = self.scrollarea_sim_detector
        case "PerfectlyMatchedLayer":
          container = None
          if object[0] != None:
            assert self.pml_thickness is not None
            self.pml_thickness.value = object[0]
        case _:
          container = None

      if container is not None:
        with container:
          with ui.row() as row:
            ui.button(object[0], on_click=lambda e=object[0]: self.controller.choose_box(e), color=None).props('flat')
            ui.button(icon='delete', on_click=lambda e=object[0]: self.controller.delete_object(e), color=None).props('flat')
        self.view.row_list.append(row)
      
    def scrollarea_add_material(self, obj):
      '''
      adds material to the material scrollarea
      param obj: tuple with (name, material, is_custom)
      type obj: tuple
      '''
      with self.scrollarea_materials:
          with ui.row() as row:
            ui.button(obj[0], on_click=lambda e=obj: self.controller.view_material(e), color=None).props('flat')
            if obj[2]:
              ui.button(icon='delete', on_click=lambda object= obj: self.delete_material(object), color=None).props('flat')

      
    def update_materials(self):
      '''
      clears and rebuilds the material scrollarea
      ''' 
      self.scrollarea_materials.clear()
      for obj in self.controller.model.material.material_list:
                self.scrollarea_add_material(obj)
    
    def delete_material(self, material):
      '''
      handler for deleting custom materials, prevents removal of materials still in use
      param material: tuple with (name, material, is_custom)
      type material: tuple
      '''
      IsUsed = False
      usedIn = []
      for obj in self.controller.project.objects:
        if type(obj) == UniformMaterialObject or type(obj) == SimulationVolume:
          if self.controller.model.material.get_name_from_material(obj.material) == material[0]:
            IsUsed = True
            usedIn.append(obj)

      if IsUsed:
        with ui.dialog() as dialog, ui.card():
          ui.label("Unable to delete material: " + material[0] + ". Material is used in the following objects:")
          for obj in usedIn:
            ui.label(obj.name).style('color: red')
          ui.label('Please remove the material from all objects before deleting')
          ui.button('Close',on_click= dialog.close)
        dialog.open()
      else:
        self.controller.model.material.remove_material(material)
        self.update_materials()

    def update(self, objects):
      '''
      clears and rebuilds entire left drawer basend on data in project
      param objects: list of tuples with (name, type)
      type objects: list
      '''
      self.clear_drawer()
      self.update_materials()
      for i in objects:
        self.scrollarea_add_Object(i)
      