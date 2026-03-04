from nicegui import ui, events
from fdtdx_studio.ui.scene_3d.koor import CoordinateSystem
from fdtdx_studio.ui.ui_elements.view_helper import ViewHelper

def scale_number(float_rgb):
    int_rgb = []
    for val in float_rgb:
      int_rgb.append(int(255 * val))

    return tuple(int_rgb)
    #return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def rgb_to_hex(rgb):
  return '#%02x%02x%02x' % scale_number(rgb)


class MainSection:
  def __init__(self, controller):
    self.objects = {}
    self.colors = {}
    self.controller = controller
    self.camera_distance_base = (10, 0, 10)
    self.unit_scale = 1000000 # 1 unit = 1 micrometer

    with ui.element().classes('w-full h-[90vh] flex flex-col top-0'):
      with ui.scene(grid=False, show_stats=False, on_click=self.handle_click).style(
        'position: absolute; top: 0; left: 0; width: 100%; height: 100%;'
        'z-index: 1;'
      ) as self.scene:
        pass

      ViewHelper(self.scene)

      ui.button(icon='center_focus_strong', on_click=self.center_view).props('flat').style(
        'position: absolute; bottom: 1%; right: 1%; width: 5%; height: 5%;'
        'z-index: 2;'
      ).tooltip('Center Scene')

      
  
  def center_view(self):
    x, y, z = self.camera_distance_base
    self.scene.move_camera(x=x, y=y, z=z, look_at_x=0, look_at_y=0, look_at_z=0, duration=0)
  
  def add_object(self, obj):
    with self.scene:
      if isinstance(obj[4], tuple):
        self.colors[obj[0]] = rgb_to_hex(obj[4])
        box = ui.scene.box(obj[2][0]*self.unit_scale, obj[2][1]*self.unit_scale, obj[2][2]*self.unit_scale).move(obj[3][0]*self.unit_scale, obj[3][1]*self.unit_scale, obj[3][2]*self.unit_scale).material(rgb_to_hex(obj[4]))
      else:
        self.colors[obj[0]] = obj[4]
        box = ui.scene.box(obj[2][0]*self.unit_scale, obj[2][1]*self.unit_scale, obj[2][2]*self.unit_scale).move(obj[3][0]*self.unit_scale, obj[3][1]*self.unit_scale, obj[3][2]*self.unit_scale).material(obj[4])

    self.objects[obj[0]] = box.with_name(obj[0])


  #clear the entire 3d scene and then add all objects in der objectlist
  def update(self, objects):
    self.scene.clear()
    self.objects.clear()
    self.add_simulation_volume(objects[0])
    for obj in objects[1:]:#remove [1:] if simulation volume should also be drawn
      if obj[1] != "PerfectlyMatchedLayer":
        self.add_object(obj)

  def delete_object(self, name):
    self.objects[name].delete()
    return self.objects.pop(name)
  
  def change_color(self, name, color):
    if isinstance(color, tuple):
      self.colors.update({name: rgb_to_hex(color)})
      self.objects[name].material(self.colors[name])
    else:
      self.colors[name].update({name: color})
      self.objects[name].material(color)

  #TODO: depricate?
  def scale_scene_object(self, name, x, y, z):
    if self.objects is not None:
      self.objects[name].scale(x*self.unit_scale, y*self.unit_scale, z*self.unit_scale)
  
  #TODO: depricate?
  def move_scene_object(self, name, x, y, z):
    self.objects[name].move(x*self.unit_scale, y*self.unit_scale, z*self.unit_scale)

  def highlight(self, name):
    self.downplay()
    for n, obj in self.objects.items():
      if n not in [name,'Simulation_Volume']:
        obj.material(opacity=0.4, color=self.colors[n])

  def downplay(self):
    for key, value in self.objects.items():
      if value != self.objects['Simulation_Volume']:
        value.material(opacity=1, color=self.colors[key])
  
  def add_simulation_volume(self, volume):
    volume_units = (volume[2][0]*self.unit_scale, volume[2][1]*self.unit_scale, volume[2][2]*self.unit_scale)
    with self.scene:
      box = ui.scene.box(1,1, 1, wireframe=True).material('#888888')
    box.scale(*volume_units)
    self.camera_distance_base = (volume_units[0]*1.2, 0, 0) # adjust camera distance based on volume size
    self.center_view()
    self.objects['Simulation_Volume'] = box
  
  def handle_click(self, e: events.SceneClickEventArguments):
    name = next((hit.object_name for hit in e.hits if hit.object_name), None)
    if name is not None:
      self.controller.choose_box(name)
