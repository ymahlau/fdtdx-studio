from nicegui import ui
from fdtdx_studio.ui.popups.new_pop_up import new_pop_up as NewPopUp
from typing import Any, cast

class pop_up_new_object(NewPopUp):
  """Popup for creating a new simulation object."""

  def __init__(self, controller):
    super().__init__(controller)
    # Define the button function for adding a new object
    self.button_function = self._on_add_object
    self.button_label = 'Add Simulation Object'

    self.pop_up_new_object = None
    self.build_dialog()  

  def _on_add_object(self):
    assert self.input_name is not None
    assert self.input_length is not None
    assert self.input_width is not None
    assert self.input_height is not None
    self.controller.add_object(
          popup=self,
          name=self.input_name.value,
          length=self.input_length.value,
          width=self.input_width.value,
          height=self.input_height.value,
          color=self.input_color,
          material = self.input_material,
          typ='scrollarea_sim_objects',
        )
    
  def build_dialog(self):
    """Builds the dialog UI for the popup. (Overrides superclass method)"""
    with ui.dialog() as self.pop_up_new_object, ui.card():
      with ui.column():
        self.build_common_ui()

        # Objekt-spezifisch
        with ui.dropdown_button('Material').classes('w-full') as self.material_show:
          for obj in self.material.material_list:
            ui.item(text=obj[0], on_click= lambda material=obj: self.choose_material(material))

        self.add_button(self.button_function, self.button_label)      
  
  
  #helper methods for the popup
  def pick_color(self, color, name):
    self.input_color = color
    assert self.color_show is not None
    cast(Any, self.color_show).close()
    cast(Any, self.color_show).text = name

  def choose_material(self, material):
    self.input_material = material[1]
    self.material_show.close()
    self.material_show.text = material[0]

  def open_new_object_popup(self):
    assert self.pop_up_new_object is not None
    self.pop_up_new_object.open()  
  
  def close_self(self):
    # reset popup values
    cast(Any, self.color_show).text = 'Color: Red'
    self.input_color = 'Red'
    cast(Any, self.input_length).value = 1
    cast(Any, self.input_width).value = 1
    cast(Any, self.input_height).value = 1
    assert self.pop_up_new_object is not None
    self.pop_up_new_object.close()
  