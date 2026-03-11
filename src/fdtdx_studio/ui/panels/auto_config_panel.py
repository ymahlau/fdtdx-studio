from nicegui import ui
from fdtdx_studio.ui.panels.object_config_panel import ObjectConfigPanel
from fdtdx_studio.ui.ui_elements.attribute_elements import (
    AttributeElement, NumberElement, StringElement, BooleanElement, 
    SelectElement, ColorElement, NestedObjectElement, Vector3Element, MultiSelectElement
)
from fdtdx_studio.ui.attribute_definitions import OBJECT_DEFINITIONS, AttributeDef
from typing import Dict, Any, List, Optional
import inspect
import copy

def safe_deepcopy(obj):
    """
    Safely deepcopy a dictionary or object. 
    If copy.deepcopy fails (e.g., on frozen pytreeclass instances), 
    fallback to a shallow copy or recursively copy dicts.
    """
    try:
        return copy.deepcopy(obj)
    except (TypeError, AttributeError):
        if isinstance(obj, dict):
            return {k: safe_deepcopy(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [safe_deepcopy(v) for v in obj]
        elif isinstance(obj, tuple):
            return tuple(safe_deepcopy(v) for v in obj)
        
        try:
            return copy.copy(obj)  # Fallback to shallow copy if possible
        except (TypeError, AttributeError):
            return obj  # Return reference only as a last resort

class AutoConfigPanel(ObjectConfigPanel):
    """
    Panel that automatically constructs UI input elements based on 
    AttributeDef metadata.
    """
    def __init__(self, view, controller, object_type_name: str):
        # We call super init to keep reference to view/controller and potentially usage of helper methods.
        super().__init__(view, controller)
        self.object_type_name = object_type_name
        self.elements: Dict[str, AttributeElement] = {}
        self.local_data: Dict[str, Any] = {}
        self.nav_stack: List[tuple] = [] # List of (key, type_name)
        self.current_nested_path: List[str] = [] 
        self.main_panel_container = None
        self.save_button = None
        
    def render_into(self, panel):
        """Overrides ObjectConfigPanel.render_into to use automatic construction."""
        self.main_panel_container = panel
        self._render_current_level()

    def _render_current_level(self):
        """Renders the current level (top or nested)."""
        if self.main_panel_container is None:
            return
            
        self.main_panel_container.clear()
        
        current_type = self._get_current_type_name()
        
        # Title handling
        title = f"{current_type} Configuration"
        
        with self.main_panel_container:
            # Navigation Header if nested
            if self.current_nested_path:
                with ui.row().classes('w-full items-center gap-2 mb-2'):
                    ui.button(icon='arrow_back', on_click=self._navigate_back).props('flat round dense')
                    ui.label(" / ".join(self.current_nested_path)).style('font-weight: bold')
            else:
                 pass

            definitions = OBJECT_DEFINITIONS.get(current_type, [])
            if not definitions:
                pass

            # Sort by importance
            important_defs = [d for d in definitions if d.importance > 0]
            less_important_defs = [d for d in definitions if d.importance <= 0]
            
            with ui.column().classes('w-full gap-2 p-2'):
                for definition in important_defs:
                    self._create_element(definition)
                
                if less_important_defs:
                     with ui.expansion('Show More').classes('w-full'):
                         with ui.column().classes('w-full gap-2'):
                             for definition in less_important_defs:
                                 self._create_element(definition)
            
            if not self.current_nested_path:
                ui.separator().classes('my-2')
                self.save_button = ui.button('Apply', on_click=self.on_save_clicked)

    def _create_element(self, definition: AttributeDef):
        """Creates and registers a UI element."""
        key = definition.name
        current_val = self._get_current_value(key, definition.default)
        
        # Specific validation or callback
        validation_cb = None
        if key == 'name' and not self.current_nested_path: # Top level name
             pass 

        element = None
        
        # Build callback
        def on_change_cb(val):
            self._update_param(key, val)
            if key == 'name' and not self.current_nested_path:
                self.validate_name(val) # Uses logic from base
        
        if definition.ui_type == 'number':
            element = NumberElement(definition.label, current_val, on_change_cb, tooltip=definition.tooltip)
        elif definition.ui_type == 'string':
            element = StringElement(definition.label, current_val, on_change_cb, tooltip=definition.tooltip)
        elif definition.ui_type == 'boolean':
            element = BooleanElement(definition.label, current_val, on_change_cb, tooltip=definition.tooltip)
        elif definition.ui_type == 'select':
            element = SelectElement(definition.label, current_val, on_change_cb, options=definition.options or [], tooltip=definition.tooltip)
        elif definition.ui_type == 'multi_select':
            element = MultiSelectElement(definition.label, current_val, on_change_cb, options=definition.options or [], tooltip=definition.tooltip)
        elif definition.ui_type == 'color':
             element = ColorElement(definition.label, current_val, on_change_cb, tooltip=definition.tooltip)
        elif definition.ui_type == 'vector3':
             element = Vector3Element(definition.label, current_val, on_change_cb, tooltip=definition.tooltip)
        elif definition.ui_type == 'material_select':
             # Custom logic for material selection using controller
             mat_list = self.controller.model.material.material_list
             # Options: name -> name. We display names.
             options = [m[0] for m in mat_list]
             # Helper to find object
             name_to_obj = {m[0]: m[1] for m in mat_list}
             
             # Determine current name from current_val (object)
             current_name = None
             if current_val:
                 current_name = self.controller.model.material.get_name_from_material(current_val)
             
             def on_mat_change(new_name):
                 obj = name_to_obj.get(new_name)
                 # Update param with the OBJECT, not the name
                 self._update_param(key, obj)
                 
             element = SelectElement(definition.label, current_name, on_mat_change, options=options, tooltip=definition.tooltip)
        elif definition.ui_type == 'nested':
             element = NestedObjectElement(definition.label, current_val, on_change_cb, on_navigate=lambda: self._navigate_to(key, definition.target_cls), tooltip=definition.tooltip)
        
        if element:
            self.elements[key] = element
            rendered = element.render()
            
            # Hook up existing validation display from ObjectConfigPanel if 'name'
            if key == 'name' and not self.current_nested_path:
                 self.name = rendered # Map to base class expectation if needed
                 # Add the error label from base class
                 self.name_error = ui.label('This Name is already in use').style('color: red')
                 self.name_error.set_visibility(False)


    def _get_current_type_name(self):
         if not self.nav_stack:
             return self.object_type_name
         return self.nav_stack[-1][1]

    def _get_current_value(self, key, default):
        data = self.local_data
        for nav_key, _ in self.nav_stack:
             data = data.get(nav_key, {})
             if data is None: 
                data = {}
        return data.get(key, default)

    def _update_param(self, key, value):
        # Update self.local_data
        # We need to traverse down
        data = self.local_data
        path = [n[0] for n in self.nav_stack] # List of keys
        
        for nav_key in path:
            if nav_key not in data or data[nav_key] is None:
                data[nav_key] = {}
            data = data[nav_key]
        
        data[key] = value

    def _navigate_to(self, key, target_cls):
        self.current_nested_path.append(key)
        self.nav_stack.append((key, target_cls))
        self._render_current_level()

    def _navigate_back(self):
        if self.current_nested_path:
            self.current_nested_path.pop()
            self.nav_stack.pop()
            self._render_current_level()
    def update_values(self, parameters: Dict[str, Any]):
        """Updates the panel with new parameters from the controller/model."""
        self.local_data = safe_deepcopy(parameters)
        self.nav_stack = [] 
        self.current_nested_path = []
        self._render_current_level()
        
        # We also need to set base class 'original_name' for validation
        if 'name' in parameters:
            self.original_name = parameters['name']

    def get_parameters(self) -> Dict[str, Any]:
        return self.local_data

    def on_save_clicked(self):
        """Dispatch save to controller."""
        # Using dispatch table or match
        
        params = self.get_parameters().copy()
        # Remove metadata keys that shouldn't be passed to save methods
        params.pop('names', None)
        params.pop('constraints', None)
        
        method_map = {
            'GaussianPlaneSource': self.controller.saveGaussianPlaneSourceParams,
            'ModePlaneSource': self.controller.saveModePlaneSourceParams,
            'UniformMaterialObject': self.controller.saveParams, 
            'EnergyDetector': self.controller.saveEnergyDetectorParams,
            'FieldDetector': self.controller.saveFieldDetectorParams,
            'PoyntingFluxDetector': self.controller.savePoyntingFluxDetectorParams,
            'ModeOverlapDetector': self.controller.saveModeOverlapDetectorParams,
            'PhasorDetector': self.controller.savePhasorDetectorParams,
        }
        
        saver = method_map.get(self.object_type_name)
        if saver:
            saver(params)
        else:
            ui.notify(f"No save method for {self.object_type_name}", type='negative')
            return
            
        super().on_save_clicked() # Calls ui_update

    # Overriding apply_disable/enable to work with our button
    def apply_disable(self):
        if self.save_button:
            self.save_button.disable()

    def apply_enable(self):
        if self.save_button:
            self.save_button.enable()
