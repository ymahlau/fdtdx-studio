from nicegui import ui
from typing import Callable, Any, Optional, List, Tuple
from dataclasses import dataclass, field

@dataclass
class AttributeElement:
    """Base class for all attribute UI elements."""
    label: str
    value: Any
    on_change: Callable[[Any], None]
    tooltip: Optional[str] = None
    element: Any = field(init=False, default=None)

    def render(self):
        """Renders the UI element. Must be implemented by subclasses."""
        raise NotImplementedError

    def update(self, value: Any):
        """Updates the UI element with a new value."""
        self.value = value
        if self.element:
            self.element.value = value

@dataclass
class NumberElement(AttributeElement):
    """UI element for float/int values."""
    step: float = 1.0
    format: str = '%.2f'

    def render(self):
        self.element = ui.number(self.label, value=self.value, step=self.step, format=self.format, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full').props('dense')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

@dataclass
class StringElement(AttributeElement):
    """UI element for string values."""
    def render(self):
        self.element = ui.input(self.label, value=self.value, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full').props('dense')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

@dataclass
class BooleanElement(AttributeElement):
    """UI element for boolean values."""
    def render(self):
        self.element = ui.checkbox(self.label, value=self.value, on_change=lambda e: self.on_change(e.value))
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

@dataclass
class SelectElement(AttributeElement):
    """UI element for selecting from a list of options."""
    options: List[Any] = field(default_factory=list)

    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], options: List[Any], tooltip: Optional[str] = None):
        super().__init__(label, value, on_change, tooltip)
        self.options = options

    def render(self):
        self.element = ui.select(self.options, label=self.label, value=self.value, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

@dataclass
class MultiSelectElement(AttributeElement):
    """UI element for selecting multiple items from a list."""
    options: List[Any] = field(default_factory=list)

    def __init__(self, label: str, value: Any, on_change: Callable[[Any], None], options: List[Any], tooltip: Optional[str] = None):
        super().__init__(label, value, on_change, tooltip)
        self.options = options
        self.__post_init__()

    def __post_init__(self):
        if self.value is None:
            self.value = []

    def render(self):
        self.element = ui.select(self.options, label=self.label, value=self.value, multiple=True, on_change=lambda e: self.on_change(e.value))
        self.element.classes('w-full')
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

@dataclass
class ColorElement(AttributeElement):
    """UI element for color selection using a predefined palette."""
    def __post_init__(self):
        self.preset_colors = {
            'Red': '#FF0000',
            'Green': '#00FF00',
            'Blue': '#0000FF',
            'Orange': '#FFA500',
            'Purple': '#800080',
            'Cyan': '#00FFFF',
            'Pink': '#FFC0CB',
            'Yellow': '#FFFF00',
            'Gray': '#808080',
            'Black': '#000000',
        }
        self.reverse_preset_colors = {
            v.lower(): k for k, v in self.preset_colors.items()
        }

    def render(self):
        initial_color = self._normalize_hex(self.value) or '#FF0000'
        initial_name = self._get_color_name(initial_color)

        with ui.column().classes('w-full gap-1') as self.element:
            if self.label:
                ui.label(self.label)

            with ui.row().classes('w-full items-end gap-2 no-wrap'):
                # preset color selection
                self.color_select = ui.select(
                    options=list(self.preset_colors.keys()),
                    label='Color',
                    value=initial_name if initial_name in self.preset_colors else None,
                    on_change=lambda e: self.set_color_by_name(e.value),
                ).classes('w-17')

                # color input
                self.color_input = ui.color_input(
                    '',
                    value=initial_color,
                    on_change=lambda e: self.on_color_input_change(e.value),
                ).classes('w-30')

                # color preview
                self.color_preview = ui.html(
                    self._preview_html(initial_color)
                ).classes('shrink-0')

        if self.tooltip:
            self.element.tooltip(self.tooltip)

        self.value = initial_color
        return self.element

    def set_color_by_name(self, color_name: str):
        if not color_name:
            return
        color_hex = self.preset_colors.get(color_name)
        if not color_hex:
            return
        self._set_color(color_hex, update_select=True, trigger_callback=True)

    def on_color_input_change(self, color_hex: str):
        self._set_color(color_hex, update_select=True, trigger_callback=True)

    def _set_color(self, color_hex: str, update_select: bool = True, trigger_callback: bool = True):
        normalized = self._normalize_hex(color_hex)
        if not normalized:
            return

        self.value = normalized

        if hasattr(self, 'color_input') and self.color_input:
            self.color_input.value = normalized

        if hasattr(self, 'color_preview') and self.color_preview:
            self.color_preview.content = self._preview_html(normalized)
            self.color_preview.update()

        if update_select and hasattr(self, 'color_select') and self.color_select:
            color_name = self._get_color_name(normalized)
            self.color_select.value = color_name if color_name in self.preset_colors else None
            self.color_select.update()

        if trigger_callback and self.on_change:
            self.on_change(normalized)

    def update(self, value: Any):
        normalized = self._normalize_hex(value)
        if not normalized:
            return
        self._set_color(normalized, update_select=True, trigger_callback=False)

    def _get_color_name(self, hex_code: str) -> str:
        if not hex_code:
            return 'Color'
        return self.reverse_preset_colors.get(hex_code.lower(), hex_code)

    def _normalize_hex(self, hex_code: Any) -> str | None:
        if not hex_code:
            return None
        hex_code = str(hex_code).strip()
        if not hex_code.startswith('#'):
            hex_code = f'#{hex_code}'
        if len(hex_code) != 7:
            return None
        return hex_code.upper()

    def _preview_html(self, color_hex: str) -> str:
        return f'''
        <div style="
            width: 36px;
            height: 36px;
            min-width: 36px;
            min-height: 36px;
            border-radius: 6px;
            border: 1px solid #ccc;
            background-color: {color_hex};
        "></div>
        '''

@dataclass
class NestedObjectElement(AttributeElement):
    """UI element for navigating to a nested object's configuration."""
    on_navigate: Callable[[], None] = None
    
    def render(self):
        with ui.row().classes('w-full items-center justify-between'):
            ui.label(self.label)
            self.element = ui.button(icon='arrow_forward', on_click=self.on_navigate).props('flat round dense')
        
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

@dataclass
class Vector3Element(AttributeElement):
    """UI element for 3D vector values (x, y, z)."""
    def __post_init__(self):
        if not self.value:
            self.value = (0.0, 0.0, 0.0)

    def render(self):
        with ui.column().classes('w-full') as self.element:
            ui.label(self.label).classes('text-sm font-bold')
            with ui.row().classes('w-full flex-nowrap gap-1'):
                self.x = ui.number('x', value=self.value[0], on_change=lambda e: self._on_component_change(0, e.value)).classes('flex-1').props('dense')
                self.y = ui.number('y', value=self.value[1], on_change=lambda e: self._on_component_change(1, e.value)).classes('flex-1').props('dense')
                self.z = ui.number('z', value=self.value[2], on_change=lambda e: self._on_component_change(2, e.value)).classes('flex-1').props('dense')
        
        if self.tooltip:
            self.element.tooltip(self.tooltip)
        return self.element

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
