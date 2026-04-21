from nicegui import ui
from fdtdx_studio.ui.popups.pop_up_constraints import Pop_up_constraints

class ObjectConfigPanel():
  '''Superclass of all object config panels
  Fuction: Visualises all common parameters and creates interface for more specific parameters.
  '''

  def __init__(self, view, controller):
        """Initializes the ObjectConfigurationPanel with references to the main view and controller."""
        self.controller = controller
        self.view = view
        # Parameter helpers
        self.color = None

        # Widget references

        # name
        self.name = None
        self.original_name = None

        # color widget
        self.color_changer = None

        # partial_real_position widgets
        self.partial_real_position_x = None
        self.partial_real_position_y = None
        self.partial_real_position_z = None


        # partial_grid_shape widgets
        self.partial_grid_shape_x = None
        self.partial_grid_shape_y = None
        self.partial_grid_shape_z = None
  
        # partial_real_shape widgets
        self.partial_real_shape_x = None
        self.partial_real_shape_y = None
        self.partial_real_shape_z = None

        # max_random_real_offsets widgets
        self.max_random_real_offsets_x = None
        self.max_random_real_offsets_y = None
        self.max_random_real_offsets_z = None

        # max_random_grid_offsets widgets
        self.max_random_grid_offsets_x = None
        self.max_random_grid_offsets_y = None
        self.max_random_grid_offsets_z = None

        # material
        self.material = None

        #widget-list for iteration
        self.widget_list = [self.name,
                            self.color_changer,
                            self.partial_real_position_x,
                            self.partial_real_position_y,
                            self.partial_real_position_z,
                            self.partial_grid_shape_x,
                            self.partial_grid_shape_y,
                            self.partial_grid_shape_z,
                            self.partial_real_shape_x,
                            self.partial_real_shape_y,
                            self.partial_real_shape_z,
                            self.max_random_real_offsets_x,
                            self.max_random_real_offsets_y,
                            self.max_random_real_offsets_z,
                            self.max_random_grid_offsets_x,
                            self.max_random_grid_offsets_y,
                            self.max_random_grid_offsets_z
                            ]
        
        #widget for constraints
        self.constrains = None
        self.scroll_area_con = None
        self.name_of_all_objects = []
        self.cons = {}
        self.pop_up_con = Pop_up_constraints(self)
        self.scroll_row = {}

  def render_into(self, panel):
    """Render the configuration UI inside the given panel (clears first)."""
    if panel is None:
      ui.notification('No panel found to render config panel into', color='red')
      return
    panel.clear()
    with panel:
      with ui.column().classes('w-full gap-2 p-2'):
          
        self.name = ui.input('Name', on_change= lambda e: self.validate_name(e.value)).classes('w-full')
        self.name_error = ui.label('This Name is already in use').style('color: red')
        self.name_error.set_visibility(False)

        ui.label('Partial Real Position').style('font-size: 13px; font-weight: bold;').tooltip("Sets center of box in relation to the simulation volume in real coordinates.")
        with ui.row().classes('w-full flex-nowrap gap-1'):
          self.partial_real_position_x = ui.number('x', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          self.partial_real_position_y = ui.number('y', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          self.partial_real_position_z = ui.number('z', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
            
        ui.label('Partial Real Shape').style('font-size: 13px; font-weight: bold;').tooltip("Sets the size of the box in real coordinates.")
        with ui.row().classes('w-full flex-nowrap gap-1'):
          self.partial_real_shape_x = ui.number('x', value=1, min=0,step= 1e-6, validation=self._validate_shape).classes('flex-1').props('dense')
          self.partial_real_shape_y = ui.number('y', value=1, min=0,step= 1e-6, validation=self._validate_shape).classes('flex-1').props('dense')
          self.partial_real_shape_z = ui.number('z', value=1, min=0,step= 1e-6, validation=self._validate_shape).classes('flex-1').props('dense')

        ui.label('Partial Grid Shape').style('font-size: 13px; font-weight: bold;').tooltip("Sets the size of the box in grid coordinates.")
        with ui.row().classes('w-full flex-nowrap gap-1'):
          self.partial_grid_shape_x = ui.number('x', value=0, min=0,step= 1e-6).classes('flex-1').props('dense')
          self.partial_grid_shape_y = ui.number('y', value=0,step= 1e-6, min=0).classes('flex-1').props('dense')
          self.partial_grid_shape_z = ui.number('z', value=0,step= 1e-6, min=0).classes('flex-1').props('dense')

        ui.label('Max Random Real Offsets').style('font-size: 13px; font-weight: bold;').tooltip("Maximum random offset in real coordinates.")
        with ui.row().classes('w-full flex-nowrap gap-1'):
          self.max_random_real_offsets_x = ui.number('x', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          self.max_random_real_offsets_y = ui.number('y', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          self.max_random_real_offsets_z = ui.number('z', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')

        ui.label('Max Random Grid Offsets').style('font-size: 13px; font-weight: bold;').tooltip("Maximum random offset in grid coordinates.")
        with ui.row().classes('w-full flex-nowrap gap-1'):
          self.max_random_grid_offsets_x = ui.number('x', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          self.max_random_grid_offsets_y = ui.number('y', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          self.max_random_grid_offsets_z = ui.number('z', value=0,step= 1e-6, validation=self._validate_float).classes('flex-1').props('dense')
          
        with ui.dropdown_button('Color').classes('w-full') as self.color_changer:
          ui.item('Red', on_click=lambda: self.change_color('#FF0000', 'Red'))
          ui.item('Green', on_click=lambda: self.change_color('#00FF00', 'Green'))
          ui.item('Blue', on_click=lambda: self.change_color('#0000FF', 'Blue'))
          ui.item('Orange', on_click=lambda: self.change_color('#FFA500', 'Orange'))
          ui.item('Purple', on_click=lambda: self.change_color('#800080', 'Purple'))
          ui.item('Cyan', on_click=lambda: self.change_color('#00FFFF', 'Cyan'))
          ui.item('Pink', on_click=lambda: self.change_color('#FFC0CB', 'Pink'))
          ui.item('Yellow', on_click=lambda: self.change_color('#FFFF00', 'Yellow'))
          ui.item('Gray', on_click=lambda: self.change_color('#808080', 'Gray'))
          ui.item('Black', on_click=lambda: self.change_color('#000000', 'Black'))

        with ui.expansion('Contstrains').classes('w-full') as self.constrains:
          with self.constrains.add_slot('header'):
            with ui.row().classes('w-full items-center justify-between'):
                ui.label('Constrains').style('font-size: 15px')
                ui.button(icon='add', color = None, on_click=lambda: self.pop_up_con.open_pop_up('new_con', self.name_of_all_objects)).props('flat').style('pointer-events: auto; z-index: 10')
          with ui.scroll_area().classes('w-full h-48 ml-4') as self.scroll_area_con:
              pass

  def get_parameters(self):
    '''
    Collect the current parameter values from the UI input fields and return them as a dictionary.
    :return: Dictionary of current parameter values.
    :rtype: dict
    '''
    parameters = {}
    partial_real_position = (self.partial_real_position_x.value if self.partial_real_position_x else None,
                             self.partial_real_position_y.value if self.partial_real_position_y else None,
                             self.partial_real_position_z.value if self.partial_real_position_z else None)
    
    partial_real_shape = (self.partial_real_shape_x.value if self.partial_real_shape_x else None,
                          self.partial_real_shape_y.value if self.partial_real_shape_y else None,
                          self.partial_real_shape_z.value if self.partial_real_shape_z else None)
    
    partial_grid_shape = (self.partial_grid_shape_x.value if self.partial_grid_shape_x else None,
                           self.partial_grid_shape_y.value if self.partial_grid_shape_y else None,
                           self.partial_grid_shape_z.value if self.partial_grid_shape_z else None)
    
    max_random_real_offsets = (self.max_random_real_offsets_x.value if self.max_random_real_offsets_x else None,
                               self.max_random_real_offsets_y.value if self.max_random_real_offsets_y else None,
                               self.max_random_real_offsets_z.value if self.max_random_real_offsets_z else None)
    
    max_random_grid_offsets = (self.max_random_grid_offsets_x.value if self.max_random_grid_offsets_x else None,
                               self.max_random_grid_offsets_y.value if self.max_random_grid_offsets_y else None,
                               self.max_random_grid_offsets_z.value if self.max_random_grid_offsets_z else None)
    
    parameters['name'] = self.name.value if self.name else None
    parameters['partial_real_position'] = partial_real_position
    parameters['partial_real_shape'] = partial_real_shape
    parameters['partial_grid_shape'] = partial_grid_shape
    parameters['max_random_real_offsets'] = max_random_real_offsets
    parameters['max_random_grid_offsets'] = max_random_grid_offsets
    parameters['color'] = self.color
    self.controller.save_constraints(self.original_name, list(self.cons.values()))
    self.set_name(self.name.value if self.name else None)
    return parameters

  def update_values(self, parameters):
    """
    Update the UI input fields based on the provided parameters dictionary.
    :param parameters: Dictionary containing parameter values to update the UI with.
    :type parameters: dict
    """
    self.set_name(parameters.get('name', ''))
    self.set_partial_real_position(*parameters.get('partial_real_position', (0, 0, 0)))
    self.set_partial_real_shape(*parameters.get('partial_real_shape', (1, 1, 1)))
    self.set_partial_grid_shape(*parameters.get('partial_grid_shape', (0, 0, 0)))
    self.set_max_random_real_offsets(*parameters.get('max_random_real_offsets', (0, 0, 0)))
    self.set_max_random_grid_offsets(*parameters.get('max_random_grid_offsets', (0, 0, 0)))
    self.set_material(parameters.get('material', None))
    color_hex = parameters.get('color', '#FFFFFF')
    color_name = self.convert_color_hex_to_name(color_hex)
    self.change_color(color_hex, color_name)
    self.name_of_all_objects = parameters['names']
    for con in parameters['constraints']:
      self.add_con_to_scroll_and_dict(con)

  def save_con(self, con):
    if con['new']:
      con['new'] = False
      self.add_con_to_scroll_and_dict(con)
    else:
      self.cons[con['key']].update(con)
  

  def add_con_to_scroll_and_dict(self, con):
    self.cons[con['key']] = con
    if self.scroll_area_con is None:
      return  
    with self.scroll_area_con:
      with ui.row() as row:
        ui.button(con['key'], on_click=lambda: self.pop_up_con.open_pop_up(con['type'], self.name_of_all_objects, con), color=None).props('flat')
        ui.button(icon='delete', on_click=lambda e = con['key']: self.delete_con(e), color=None).props('flat')
    
    self.scroll_row[con['key']] = row
      


  def delete_con(self, name):
    self.scroll_row[name].delete()
    self.scroll_row.pop(name)
    self.cons.pop(name)

  def _validate_shape(self, value):
    if not value:
      return
    if float(value) < 0:
      self.view.send_error("Invalid size: negative sizes are not available.", 500)

  def _validate_float(self, value) -> str | None:
      """Validation function to check if input is a float or empty."""
      try:
          float(value)
          return None
      except (ValueError, TypeError):
          if value != None:
            return 'Must be a number'
          return None
      
  def validate_name(self, name:str):
    '''Validates the name to guarantee the name does not already exist'''
    if name != self.original_name:
      if self.controller.model.name_is_object_X(name):
        self.name_error.set_text("Objects cannot be named Object_X")
        self.name_error.set_visibility(True)
        self.apply_disable()
      else:
        if name != self.controller.model.namecheck(name):
          self.name_error.set_text("This Name is already in use")
          self.name_error.set_visibility(True)
          self.apply_disable()
        else:
          self.name_error.set_visibility(False)
          self.apply_enable()
  
  #Functions to individualise with the panels for the Apply Buttons
  def apply_disable(self):
     None 
     #Will be set in the individual Panels

  def apply_enable(self):
     None
      
  # setter methods for individual parameters
  def set_name(self, name):
        """Update the name input field."""
        #add original name for the name validation to work correctly.
        self.original_name = name
        if self.name:
          self.name.value = name
        
  
  def set_material(self, material):
     if self.set_material:
        self.material = material

  def set_partial_real_position(self, x, y, z, verbose=False):
        """Update the partial real position input fields. Parameters: x, y, z"""
        if verbose:
          print(f"Updating partial real position label to: {x}, {y}, {z}\n")
        if self.partial_real_position_x:
          self.partial_real_position_x.value = x
        if self.partial_real_position_y:
          self.partial_real_position_y.value = y
        if self.partial_real_position_z:
          self.partial_real_position_z.value = z
  
  def set_partial_real_shape(self, x, y, z, verbose=False):
        """Update the partial real shape input fields. Parameters: x, y, z"""
        if verbose:
          print(f"Updating partial real shape label to: {x}, {y}, {z}\n")
        if self.partial_real_shape_x:
          self.partial_real_shape_x.value = x
        if self.partial_real_shape_y:
          self.partial_real_shape_y.value = y
        if self.partial_real_shape_z:
          self.partial_real_shape_z.value = z
  
  def set_partial_grid_shape(self, x, y, z, verbose=False):
        """Update the partial grid shape input fields. Parameters: x, y, z"""
        if verbose:
          print(f"Updating partial grid shape label to: {x}, {y}, {z}\n")
        if self.partial_grid_shape_x:
          self.partial_grid_shape_x.value = x
        if self.partial_grid_shape_y:
          self.partial_grid_shape_y.value = y
        if self.partial_grid_shape_z:
          self.partial_grid_shape_z.value = z
  
  def set_max_random_real_offsets(self, x, y, z, verbose=False):
        """Update the max random real offsets input fields. Parameters: x, y, z"""
        if verbose:
          print(f"Updating max random real offsets label to: {x}, {y}, {z}\n")
        if self.max_random_real_offsets_x:
          self.max_random_real_offsets_x.value = x
        if self.max_random_real_offsets_y:
          self.max_random_real_offsets_y.value = y
        if self.max_random_real_offsets_z:
          self.max_random_real_offsets_z.value = z
  
  def set_max_random_grid_offsets(self, x, y, z, verbose=False):
        """Update the max random grid offsets input fields. Parameters: x, y, z"""
        if verbose:
          print(f"Updating max random grid offsets label to: {x}, {y}, {z}\n")
        if self.max_random_grid_offsets_x:
          self.max_random_grid_offsets_x.value = x
        if self.max_random_grid_offsets_y:
          self.max_random_grid_offsets_y.value = y
        if self.max_random_grid_offsets_z:
          self.max_random_grid_offsets_z.value = z
  
  def set_color_changer_text(self, text):
        """Update the color dropdown button text. Parameters: x, y, z"""
        if self.color_changer:
            self.color_changer.text = text
  
  def change_color(self, color_hex, color_name):
        """Updates Color UI and gives controller the color_hex to change the color. """
        self.set_color_changer_text(color_name)
        self.color = color_hex
        
        if self.color_changer:
            self.color_changer.close()

  def convert_color_hex_to_name(self, color_hex):
        """
        Converts a hex color code to its corresponding color name.
        param color_hex: Hex color code as a string (e.g., '#FF0000').
        return: Corresponding color name as a string (e.g., 'Red').
        """
        color_map = {
            '#FF0000': 'Red',
            '#ff0000': 'Red',
            '#00ff00': 'Green',
            '#00FF00': 'Green',
            '#0000ff': 'Blue',
            '#0000FF': 'Blue',
            '#ffa500': 'Orange',
            '#FFA500': 'Orange',
            '#800080': 'Purple',
            '#800080': 'Purple',
            '#00ffff': 'Cyan',
            '#00FFFF': 'Cyan',
            '#ffc0cb': 'Pink',
            '#FFC0CB': 'Pink',
            '#ffff00': 'Yellow',
            '#FFFF00': 'Yellow',
            '#808080': 'Gray',
            '#808080': 'Gray',
            '#000000': 'Black',
            '#000000': 'Black'
        }
        return color_map.get(color_hex, color_hex)  # Return hex if name not found
  
  def on_save_clicked(self):
    '''
    Superclass method for handling save button click.
    This method should be overridden in subclasses to implement specific save functionality.
    '''
    self.controller.ui_update()
  