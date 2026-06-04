from fdtdx.objects.static_material.static import SimulationVolume, UniformMaterialObject
from nicegui import ui

from fdtdx_studio.ui.panels.volume_panel import volume_panel
from fdtdx_studio.ui.popups.detector_popup import DetectorPopup
from fdtdx_studio.ui.popups.pop_up_new_material import pop_up_new_material
from fdtdx_studio.ui.popups.pop_up_new_object import pop_up_new_object
from fdtdx_studio.ui.popups.pop_up_new_source import pop_up_new_source
import fdtdx
from fdtdx_studio.ui.popups.detector_popup import DetectorPopup
from fdtdx_studio.ui.popups.pop_up_new_material import pop_up_new_material

class LeftDrawer:
    """Creates the left drawer UI visible on the main view, used for creating and managing simulation components.

    Contains expansion panels for Simulation Objects, Sources, Detectors, and Materials.
    """

    def __init__(self, view, controller):
        """Initializes the LeftDrawer with references to the main view and controller."""
        self.controller = controller
        self.view = view
        # LeftDrawer manages its own popup + select elements
        self.detector_popup = DetectorPopup(controller)
        self.Volume_Panel = volume_panel(controller)
        self.sim_obj_select = None
        self.source_select = None
        self.detector_select = None
        self.material_select = None
        self.materials_dict = {}
        self.pml_thickness = None
        self.build()

    def build(self):
        """Builds the left drawer UI components."""
        with (
            ui.left_drawer(elevated=True)
            .style("background-color: #E3E3E3")
            .classes("justify-start") as self.left_drawer
        ):
            # Simulation Volume
            with ui.row().classes("w-full items-center justify-between").style("padding: 16px 16px 8px 16px;"):
                ui.label("Simulation Volume").style("font-size: 15px; font-weight: 500;")
                ui.button(icon="edit", on_click=lambda: self.Volume_Panel.Volume_panel()).props("flat dense round").tooltip("Edit Simulation Volume")

            ui.separator().style("margin: 8px 0;")

            # Simulation Objects
            with ui.row().classes("w-full items-center gap-1").style("padding: 0 16px; margin-bottom: 8px;"):
                self.sim_obj_select = ui.select(
                    options=[],
                    label="Simulation Objects",
                    on_change=lambda e: self.controller.choose_box(e.value)
                ).classes("flex-1")
                with ui.row().classes("gap-0"):
                    ui.button(
                        icon="add",
                        on_click=lambda: pop_up_new_object(self.controller).open_new_object_popup(),
                    ).props("flat dense round").tooltip("Add new object")
                    ui.button(
                        icon="delete",
                        on_click=self.delete_selected_sim_object
                    ).props("flat dense round text-red").tooltip("Delete selected object")

            # Sources
            with ui.row().classes("w-full items-center gap-1").style("padding: 0 16px; margin-bottom: 8px;"):
                self.source_select = ui.select(
                    options=[],
                    label="Sources",
                    on_change=lambda e: self.controller.choose_box(e.value)
                ).classes("flex-1")
                with ui.row().classes("gap-0"):
                    ui.button(
                        icon="add",
                        on_click=lambda: pop_up_new_source(self.controller).open_new_source_popup(),
                    ).props("flat dense round").tooltip("Add new source")
                    ui.button(
                        icon="delete",
                        on_click=self.delete_selected_source
                    ).props("flat dense round text-red").tooltip("Delete selected source")

            # Detectors
            with ui.row().classes("w-full items-center gap-1").style("padding: 0 16px; margin-bottom: 8px;"):
                self.detector_select = ui.select(
                    options=[],
                    label="Detectors",
                    on_change=lambda e: self.controller.choose_box(e.value)
                ).classes("flex-1")
                with ui.row().classes("gap-0"):
                    ui.button(
                        icon="add",
                        on_click=self.detector_popup.open,
                    ).props("flat dense round").tooltip("Add new detector")
                    ui.button(
                        icon="delete",
                        on_click=self.delete_selected_detector
                    ).props("flat dense round text-red").tooltip("Delete selected detector")

            ui.separator().style("margin: 8px 0;")

            with ui.row().classes("w-full items-center justify-between").style("padding: 0 16px; margin-bottom: 8px;"):
                ui.label("PML-Thickness:").style("font-size: 15px").classes("flex-1").props("dense")
                self.pml_thickness = ui.number(
                    value=0, min=0, on_change=lambda e: self.controller.set_pml_thickness(e.value)
                ).classes("flex-1 w-16")

            # Materials
            with ui.row().classes("w-full items-center gap-1").style("padding: 0 16px; margin-bottom: 8px;"):
                self.material_select = ui.select(
                    options=[],
                    label="Materials",
                    on_change=lambda e: self.controller.view_material(self.materials_dict.get(e.value))
                ).classes("flex-1")
                with ui.row().classes("gap-0"):
                    ui.button(
                        icon="add",
                        on_click=lambda: pop_up_new_material(self.controller).open_new_material_popup(),
                    ).props("flat dense round").tooltip("Add new material")
                    ui.button(
                        icon="delete",
                        on_click=self.delete_selected_material
                    ).props("flat dense round text-red").tooltip("Delete selected material")
            
            with ui.row().classes("w-full justify-end").style("padding: 0 16px; margin-bottom: 8px;"):
                ui.button(
                    icon="file_upload", on_click=lambda: self.controller.upload_material_list()
                ).props("flat dense round").tooltip("Upload a List of custom materials")
                ui.button(
                    icon="file_download", on_click=lambda: self.controller.download_material_list()
                ).props("flat dense round").tooltip("Download your custom Materials")

            self.update_materials()

    def delete_selected_sim_object(self):
        if self.sim_obj_select is not None and self.sim_obj_select.value:
            self.controller.delete_object(self.sim_obj_select.value)
            self.sim_obj_select.value = None
            
    def delete_selected_source(self):
        if self.source_select is not None and self.source_select.value:
            self.controller.delete_object(self.source_select.value)
            self.source_select.value = None
            
    def delete_selected_detector(self):
        if self.detector_select is not None and self.detector_select.value:
            self.controller.delete_object(self.detector_select.value)
            self.detector_select.value = None
            
    def delete_selected_material(self):
        if self.material_select is not None:
            name = self.material_select.value
            if name:
                obj = self.materials_dict.get(name)
                if obj and obj[2]:
                    self.delete_material(obj)
                else:
                    ui.notify("Cannot delete preset material", type="warning")

    def clear_drawer(self):
        """clears all options in left drawer"""
        if self.detector_select is not None:
            self.detector_select.options = []
        if self.sim_obj_select is not None:
            self.sim_obj_select.options = []
        if self.source_select is not None:
            self.source_select.options = []
        if self.pml_thickness is not None:
            self.pml_thickness.value = 0

    def scrollarea_add_Object(self, object):
        """
        adds object to the respective dropdown options
        param object: tuple with (name, type) or more elements
        type object: tuple
        """
        name, typ = object[0], object[1]
        match typ:
            case "UniformMaterialObject" | "scrollarea_sim_objects":
                if self.sim_obj_select is not None:
                    if name not in self.sim_obj_select.options:
                        self.sim_obj_select.options.append(name)
                        self.sim_obj_select.update()
            case "ModePlaneSource" | "GaussianPlaneSource" | "scrollarea_sim_sources":
                if self.source_select is not None:
                    if name not in self.source_select.options:
                        self.source_select.options.append(name)
                        self.source_select.update()
            case (
                "EnergyDetector"
                | "FieldDetector"
                | "ModeOverlapDetector"
                | "PhasorDetector"
                | "PoyntingFluxDetector"
                | "scrollarea_sim_detector"
            ):
                if self.detector_select is not None:
                    if name not in self.detector_select.options:
                        self.detector_select.options.append(name)
                        self.detector_select.update()
            case "PerfectlyMatchedLayer":
                if name is not None:
                    assert self.pml_thickness is not None
                    self.pml_thickness.value = name

    def update_materials(self):
        """
        clears and rebuilds the material dropdown options
        """
        if self.material_select is None:
            return
            
        self.materials_dict = {}
        options = []
        for obj in self.controller.model.material.material_list:
            name = obj[0]
            self.materials_dict[name] = obj
            options.append(name)
            
        self.material_select.options = options
        self.material_select.update()
        if self.material_select.value not in options:
            self.material_select.value = None

    def delete_material(self, material):
        """
        handler for deleting custom materials, prevents removal of materials still in use
        param material: tuple with (name, material, is_custom)
        type material: tuple
        """
        IsUsed = False
        usedIn = []
        for obj in self.controller.project.objects:
            if isinstance(obj, (UniformMaterialObject, SimulationVolume)):
                if self.controller.model.material.get_name_from_material(obj.material) == material[0]:
                    IsUsed = True
                    usedIn.append(obj)

        if IsUsed:
            with ui.dialog() as dialog, ui.card():
                ui.label("Unable to delete material: " + material[0] + ". Material is used in the following objects:")
                for obj in usedIn:
                    ui.label(obj.name).style("color: red")
                ui.label("Please remove the material from all objects before deleting")
                ui.button("Close", on_click=dialog.close)
            dialog.open()
        else:
            self.controller.model.material.remove_material(material)
            self.update_materials()

    def update(self, objects):
        """
        clears and rebuilds entire left drawer based on data in project
        param objects: list of tuples with (name, type)
        type objects: list
        """
        self.clear_drawer()
        self.update_materials()
        for i in objects:
            self.scrollarea_add_Object(i)
            
        if self.sim_obj_select is not None:
            if self.sim_obj_select.value not in self.sim_obj_select.options:
                self.sim_obj_select.value = None
            self.sim_obj_select.update()
            
        if self.source_select is not None:
            if self.source_select.value not in self.source_select.options:
                self.source_select.value = None
            self.source_select.update()
            
        if self.detector_select is not None:
            if self.detector_select.value not in self.detector_select.options:
                self.detector_select.value = None
            self.detector_select.update()
