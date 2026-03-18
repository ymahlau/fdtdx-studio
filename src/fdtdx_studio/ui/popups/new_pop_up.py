from nicegui import ui
import fdtdx

class new_pop_up():
  """Superclass for creating new pop-up dialogs for adding simulation components."""

  def __init__(self, controller):
    self.controller = controller
    self.material = self.controller.model.material
    self.input_material = fdtdx.Material()
    self.input_color = '#FF0000'
    self.input_name = None
    self.input_length = None
    self.input_width = None
    self.input_height = None
    self.color_show = None
    self.color_select = None

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

  def build_common_ui(self):
    """Builds the common UI components for the superclass popup."""

    self.input_color = '#FF0000'
    self.input_name = ui.input('Name', value='New Object',on_change= lambda e: self.validate_name(e.value))
    self.name_error = ui.label().style('color: red; font-size: 13px')
    self.name_error.set_visibility(False)
    with ui.row().classes('w-full items-end gap-2 no-wrap'):
      # dropdown for preset color selection
      self.color_select = ui.select(
          options=list(self.preset_colors.keys()),
          label='Color Select',
          value='Red',
          on_change=lambda e: self.set_color_by_name(e.value),
      ).classes('w-30')
      # color input
      self.color_show = ui.color_input(
          '',
          value=self.input_color,
          on_change=lambda e: self.on_color_input_change(e.value),
      ).classes('w-35')
      # color preview
      self.color_preview = ui.html(
          f'''
          <div style="
              width: 36px;
              height: 36px;
              min-width: 36px;
              min-height: 36px;
              border-radius: 6px;
              border: 1px solid #ccc;
              background-color: {self.input_color};
          "></div>
          '''
      ).classes('shrink-0')
    # Dimension inputs
    ui.label('Unit in m')
    self.input_width = ui.number('x', value=0.000003, step = 0.000001)
    self.input_length = ui.number('y', value=0.000003, step = 0.000001)
    self.input_height = ui.number('z', value=0.000003, step = 0.000001)

  def on_color_input_change(self, color: str) -> None:
    self.input_color = color
    self.update_color_preview()

    matched_name = next(
        (name for name, value in self.preset_colors.items() if value.lower() == color.lower()),
        None,
    )
    if matched_name and self.color_select:
        self.color_select.set_value(matched_name)

  def set_color_by_name(self, name: str) -> None:
      color = self.preset_colors[name]
      self.set_color(color)

  def set_color(self, color: str) -> None:
      self.input_color = color
      if self.color_show:
          self.color_show.set_value(color)
      self.update_color_preview()

      matched_name = next(
          (name for name, value in self.preset_colors.items() if value.lower() == color.lower()),
          None,
      )
      if matched_name and self.color_select:
          self.color_select.set_value(matched_name)

  def update_color_preview(self) -> None:
    if hasattr(self, 'color_preview') and self.color_preview:
        self.color_preview.set_content(
            f'''
            <div style="
                width: 36px;
                height: 36px;
                min-width: 36px;
                min-height: 36px;
                border-radius: 6px;
                border: 1px solid #ccc;
                background-color: {self.input_color};
            "></div>
            '''
        )

  def add_button(self, function, label='Save'):
    """Adds a button to the popup with the given function and label."""
    # Callback verzögert ausführen und aktuelle Werte verwenden
    self.save = ui.button('Save',
      on_click=  function
    ).classes('w-full').style('margin-top: 8px;').on_click(lambda: self.controller.ui_update()) 

  def validate_name(self, name:str):
    '''Validates the name to guarantee name is not already in use'''
    if hasattr(self,'save'):
      if self.controller.model.name_is_object_X(name):
        self.name_error.set_text("Objects cannot be named Object_X")
        self.name_error.set_visibility(True)
        self.save.disable()
      else:
        if name != self.controller.model.namecheck(name):
          self.name_error.set_text("This Name is already in use")
          self.name_error.set_visibility(True)
          self.save.disable()
        else:
          self.name_error.set_visibility(False)
          self.save.enable()

  def build_dialog(self):
    """Builds the dialog UI for the popup."""
    with ui.dialog() as self.new_pop_up, ui.card():
      with ui.column():
        self.build_common_ui()

  def choose_material(self, material):
    self.input_material = material

  def open_new_popup(self):
    self.new_pop_up.open()  

  def close_self(self):
        self.input_color = '#FF0000'
        if self.color_show:
            self.color_show.set_value('#FF0000')
        if self.color_select:
            self.color_select.set_value('Red')
        self.update_color_preview()
        self.input_length.value = 1
        self.input_width.value = 1
        self.input_height.value = 1
        self.new_pop_up.close()
        ui.timer(0, lambda: self.controller.ui_update(), once=True)