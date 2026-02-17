from nicegui import ui
from typing import Callable, Any, Optional, List

class AttributeElement:
    """Base class for all attribute UI elements."""
    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], tooltip: Optional[str] = None):
        self.label = label
        self.value = value
        self.on_change = on_change
        self.tooltip = tooltip
        self.element = None

    def render(self):
        """Renders the UI element. Must be implemented by subclasses."""
        raise NotImplementedError

    def update(self, value: Any):
        """Updates the UI element with a new value."""
        self.value = value
        if self.element:
            self.element.value = value

class NumberElement(AttributeElement):
    """UI element for float/int values."""
    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], tooltip: Optional[str] = None, step: float = 1.0, format: str = '%.2f'):
        super().__init__(label, value, on_change, tooltip)
        self.step = step
        self.format = format

    def render(self):
        self.element = ui.number(self.label, value=self.value, step=self.step, format=self.format, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full').props('dense')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

class StringElement(AttributeElement):
    """UI element for string values."""
    def render(self):
        self.element = ui.input(self.label, value=self.value, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full').props('dense')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

class BooleanElement(AttributeElement):
    """UI element for boolean values."""
    def render(self):
        self.element = ui.checkbox(self.label, value=self.value, on_change=lambda e: self.on_change(e.value))
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

class SelectElement(AttributeElement):
    """UI element for selecting from a list of options."""
    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], options: List[Any], tooltip: Optional[str] = None):
        super().__init__(label, value, on_change, tooltip)
        self.options = options

    def render(self):
        self.element = ui.select(self.options, label=self.label, value=self.value, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

class MultiSelectElement(AttributeElement):
    """UI element for selecting multiple items from a list."""
    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], options: List[Any], tooltip: Optional[str] = None):
        super().__init__(label, value, on_change, tooltip)
        self.options = options
        if self.value is None:
            self.value = []

    def render(self):
        self.element = ui.select(self.options, label=self.label, value=self.value, multiple=True, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

class ColorElement(AttributeElement):
    """UI element for color selection using a predefined palette."""
    def render(self):
        with ui.dropdown_button(self.label, auto_close=True).classes('w-full') as self.element:
             self.element.text = self._get_color_name(self.value)
             
             ui.item('Red', on_click=lambda: self._handle_change('#FF0000', 'Red'))
             ui.item('Green', on_click=lambda: self._handle_change('#00FF00', 'Green'))
             ui.item('Blue', on_click=lambda: self._handle_change('#0000FF', 'Blue'))
             ui.item('Orange', on_click=lambda: self._handle_change('#FFA500', 'Orange'))
             ui.item('Purple', on_click=lambda: self._handle_change('#800080', 'Purple'))
             ui.item('Cyan', on_click=lambda: self._handle_change('#00FFFF', 'Cyan'))
             ui.item('Pink', on_click=lambda: self._handle_change('#FFC0CB', 'Pink'))
             ui.item('Yellow', on_click=lambda: self._handle_change('#FFFF00', 'Yellow'))
             ui.item('Gray', on_click=lambda: self._handle_change('#808080', 'Gray'))
             ui.item('Black', on_click=lambda: self._handle_change('#000000', 'Black'))
        
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

    def _handle_change(self, color_hex, color_name):
        self.value = color_hex
        self.element.text = color_name
        self.on_change(color_hex)
        
    def update(self, value: Any):
        self.value = value
        if self.element:
            self.element.text = self._get_color_name(value)

    def _get_color_name(self, hex_code):
         color_map = {
            '#FF0000': 'Red', '#ff0000': 'Red',
            '#00FF00': 'Green', '#00ff00': 'Green',
            '#0000FF': 'Blue', '#0000ff': 'Blue',
            '#FFA500': 'Orange', '#ffa500': 'Orange',
            '#800080': 'Purple', '#800080': 'Purple',
            '#00FFFF': 'Cyan', '#00ffff': 'Cyan',
            '#FFC0CB': 'Pink', '#ffc0cb': 'Pink',
            '#FFFF00': 'Yellow', '#ffff00': 'Yellow',
            '#808080': 'Gray', '#808080': 'Gray',
            '#000000': 'Black', '#000000': 'Black'
        }
         return color_map.get(hex_code, hex_code or 'Color')

class NestedObjectElement(AttributeElement):
    """UI element for navigating to a nested object's configuration."""
    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], on_navigate: Callable[[], None], tooltip: Optional[str] = None):
         super().__init__(label, value, on_change, tooltip)
         self.on_navigate = on_navigate

    def render(self):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(self.label)
            self.element = ui.button(icon='arrow_forward', on_click=self.on_navigate).props('flat round dense')
        
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

class Vector3Element(AttributeElement):
    """UI element for 3D vector values (x, y, z)."""
    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], tooltip: Optional[str] = None):
        super().__init__(label, value, on_change, tooltip)
        if not self.value:
            self.value = (0.0, 0.0, 0.0)

    def render(self):
        with ui.column().classes('w-full'):
            ui.label(self.label).classes('text-sm font-bold')
            with ui.row().classes('w-full flex-nowrap gap-1'):
                self.x = ui.number('x', value=self.value[0], on_change=lambda e: self._on_component_change(0, e.value)).classes('flex-1').props('dense')
                self.y = ui.number('y', value=self.value[1], on_change=lambda e: self._on_component_change(1, e.value)).classes('flex-1').props('dense')
                self.z = ui.number('z', value=self.value[2], on_change=lambda e: self._on_component_change(2, e.value)).classes('flex-1').props('dense')
        
        if self.tooltip:
             # Tooltip on label or container? ui.column doesn't have tooltip in older nicegui versions maybe?
             # Assuming standard elements.
             pass
        return self.x # Return one element as representative? Or None.

    def _on_component_change(self, index, val):
        current = list(self.value)
        current[index] = val
        self.value = tuple(current)
        self.on_change(self.value)

    def update(self, value: Any):
        self.value = value if value else (0.0, 0.0, 0.0)
        if getattr(self, 'x', None):
            self.x.value = self.value[0]
            self.y.value = self.value[1]
            self.z.value = self.value[2]
