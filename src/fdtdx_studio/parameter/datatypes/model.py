#Model-class aka Logik und Daten

import fdtdx
from fdtdx import SimulationObject, SimulationVolume, ObjectContainer, UniformMaterialObject, SimulationConfig
from fdtdx_studio.constraint.constraints import Constraints
from fdtdx_studio.parameter.DType import DType
from fdtdx_studio.parameter.material.material import Material

class Model(Constraints):
    def __init__(self,object_list):
        self.current = 0
        self.track_object_list = object_list
        #self.constraints= []
        self.cache_color = 'white'
        self.container = ObjectContainer(volume_idx=0, object_list=self.track_object_list)
        self.material = Material()

    def config(self, name):
        """Sets the current index to the object with the given name."""
        for i,d in enumerate(self.track_object_list):
            if d.name == name:
                self.current = i
                return i
        return -1

  # the simulation volume should always be index 0 (and created first)
    def create_simulation_volume(self, xyz = (1e-5, 1e-5, 1e-5), material = fdtdx.Material()):
        self.track_object_list[0] = SimulationVolume(partial_real_shape=xyz,material= material, name= "Simulation Volume")
        return self.track_object_list[0]
    def update_simulation_volume(self, x: float = 1, y: float = 1, z: float =1, material = fdtdx.Material()):
        #Check if Simulation Volume exist, create it if not
        #if self.track_object_list[0] is None:
        #    self.track_object_list[0] = self.create_simulation_volume()
        self.track_object_list[0] = self.create_simulation_volume((x,y,z),material)

  # Just makes a Uniform Material Object for now
  # TODO depricate
    def create_new_dict(self, name, length, width, height):
        obj = UniformMaterialObject(partial_real_shape=(height,width,length), name=name, partial_real_position=(0,0,0)) # type: ignore

    def get_track_object_list(self):
        return self.track_object_list

    def get_current_index(self):
        return self.current
    
    def set_current_index(self, index):
        self.current = index

    def get_sources(self):
        return self.container.sources

    def get_devices(self):
        return self.container.devices

    def get_detectors(self):
        return self.container.detectors

    def rename_current(self, name):
        new = self.track_object_list[self.current].aset('name',name)
        self.track_object_list[self.current] = new

    def get_by_name(self, name):
        for obj in self.track_object_list:
            if obj.name == name:
                return obj
        return None

    def namecheck(self, name:str, index = 1):
        '''Chekcs if name already exists and if so, changes the name to name(1), name(2) etc'''
        obj = self.get_by_name(name)
        
        if obj is not None:
            if obj.name[-2] == str(index-1) and obj.name[-1] == ')':
                name = name[:-3]
            name = name.__add__('('+str(index)+')')
            index += 1
            
            return self.namecheck(name, index= index)
            
        else:
            return name
        
    def name_is_object_X(self,name):
        value = False
        if name.startswith('Object_') | name.startswith('object_'):
            value = True
        return value


    def get_current_parameters(self):

        """

        Input: None, uses the current object
        Output: Dictionary with key, value pairs, where the parameters of the object are the key and the values are the values :D

        """
        #ugly but works
        constraints = self.get_obj_constraints(self.track_object_list[self.current].name)
        names = [o.name for o in self.track_object_list if not isinstance(o, fdtdx.PerfectlyMatchedLayer) and o.name != self.track_object_list[self.current].name]
        return {**{f.name: f.value for f in self.track_object_list[self.current].get_public_fields()}, 'names':names, "constraints":constraints}
    
    def get_current_type(self):
        """
        Gets type of current object.
        """
        return type(self.track_object_list[self.current]).__name__


  # Creates a material object and appends it to the object list.
  # Partial and Real shape as a tuple-Parameter (height, width, length)!!!
    def create_material_obj(
        self, *, name=None, partial_grid_shape=None, partial_real_shape=None, partial_real_position=(0.0,0.0,0.0), color=None,
        material=None, max_random_grid_offsets=None, max_random_real_offsets=None,
        placement_order=None, verbose=False, index=None
        ):
        """Creates a UniformMaterialObject and adds it to the object list. Modifies existing object if index is provided."""
        
        if verbose:
            print(f"Creating material object: name={name}, partial_grid_shape={partial_grid_shape}, partial_real_shape={partial_real_shape}, partial_real_position={partial_real_position}, color={color}, material={material}, max_random_grid_offsets={max_random_grid_offsets}, max_random_real_offsets={max_random_real_offsets}, placement_order={placement_order}\n")
        # Map function args to the correct kwargs names


        option_map = locals()
        option_map.pop("self")
        option_map.pop("verbose")
        
        if index:
            option_map.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)


        # build kwargs only from where value is not None
        kwargs = {key: val for key, val in option_map.items() if val is not None}

        
        obj = fdtdx.UniformMaterialObject(**kwargs)
        self.real_position(obj=obj)
        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)
        return obj
    
    def create_pml_boundary_obj(self, thickness=int):
        
        # Remove existing PML boundaries
        for obj in list(self.track_object_list):
            if isinstance(obj, fdtdx.PerfectlyMatchedLayer):
                self.delete_by_object(obj)
        assert isinstance(thickness, int)
        bound_cfg = fdtdx.BoundaryConfig.from_uniform_bound(thickness=thickness, boundary_type="pml")
        bound_dict, c_list = fdtdx.boundary_objects_from_config(bound_cfg, self.track_object_list[0])
        
        for obj in bound_dict.values():
            self.track_object_list.append(obj)
        self.list_to_constraints(c_list)

    

    def create_mode_plane_source_obj(
        self, *, azimuth_angle=None, color=None, direction=None,
        elevation_angle=None, filter_pol=None, 
        max_angle_random_offset=None, max_horizontal_offset=None,
        max_random_grid_offsets=None, max_random_real_offsets=None,
        max_vertical_offset=None, mode_index=None, name=None,
        partial_grid_shape=None, partial_real_shape=None, 
        partial_real_position=(0.0,0.0,0.0), partial_grid_position=None,
        static_amplitude_factor=None, switch=None,
        temporal_profile=None, wave_character=None, index=None
        ):
        # Map args zu kwargs
        option_map = locals()
        option_map.pop("self")
        if index:
            option_map.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)

        # baue kwargs aus allen Werten, die NICHT None sind
        kwargs = {key: val for key, val in option_map.items() if val is not None}

        obj = fdtdx.ModePlaneSource(**kwargs)
        self.real_position(obj=obj)
        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)

        return obj

    
    def create_gaussian_plane_source_obj(
        self, *, azimuth_angle=None, color=None, direction=None,
        elevation_angle=None, fixed_E_polarization_vector=None,
        fixed_H_polarization_vector=None, max_angle_random_offset=None,
        max_horizontal_offset=None, max_random_grid_offsets=None,
        max_random_real_offsets=None, max_vertical_offset=None,
        name=None, normalize_by_energy=None, partial_real_position = (0.0,0.0,0.0), 
        partial_grid_position = None, partial_grid_shape=None,
        partial_real_shape=None, radius=None, static_amplitude_factor=None,
        std=None, switch=None, temporal_profile=None, wave_character=None, index=None
        ):

    # Map args → kwargs
        option_map = locals()
        option_map.pop("self")
        if index:
            option_map.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)

        # build kwargs from all non-None values
        kwargs = {key: val for key, val in option_map.items() if val is not None}

        # create the source
        obj = fdtdx.GaussianPlaneSource(**kwargs)
        self.real_position(obj=obj)

        # store it
        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)

        return obj

        

# =====================================================
#   Detector Functions
# =====================================================

    def create_energy_detector_obj(
        self, *,
        aggregate=None,
        as_slices=None,
        if_inverse_plot_backwards=None,
        inverse=None,
        partial_real_shape=None,
        partial_real_position=(0.0,0.0,0.0),
        partial_grid_shape=None,
        color=None,
        name=None,
        dtype=None,
        exact_interpolation=None,
        max_random_grid_offsets=None,
        max_random_real_offsets=None,
        num_video_workers=None,
        plot=None,
        plot_dpi=None,
        plot_interpolation=None,
        reduce_volume=None,
        switch=None,
        x_slice=None,
        y_slice=None,
        z_slice=None,
        num_time_steps_recorded=None,
        index=None
    ):
        option_map = locals()
        option_map.pop("self")
        if index:
            option_map.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)
        kwargs = {key: val for key, val in option_map.items() if val is not None}

        obj = fdtdx.EnergyDetector(**kwargs)
        self.real_position(obj=obj)
        if index:   
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)
        return obj

# reduce Volume nicht implementiert. Wollen wir das ?üwü~
    def create_field_detector_obj(
        self, *,
        color=None,
        components=None,
        dtype=None,
        max_random_grid_offsets=None,
        max_random_real_offsets=None,
        name=None,
        num_video_workers=None,
        partial_real_position=(0.0,0.0,0.0),
        partial_grid_position=None,
        partial_grid_shape=None,
        partial_real_shape=None,
        plot=None,
        plot_dpi=None,
        plot_interpolation=None,
        reduce_volume=None,
        switch=None,
        exact_interpolation=None, # Maybe default to true?! idk :3333 uwu~
        inverse=None,
        if_inverse_plot_backwards=None,
        num_time_steps_recorded=None,
        index=None
    ):
        # Alle Argumente in ein dict sammeln
        kwargs = locals()
        kwargs.pop("self")
        if index:
            kwargs.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)
        # Alle None-Werte entfernen
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        obj = fdtdx.FieldDetector(**kwargs)
        self.real_position(obj=obj)

        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)
        return obj

  

    def create_mode_overlap_detector(
        self, *,
        color=None,
        direction=None,
        dtype=None,
        exact_interpolation=None,
        filter_pol=None,
        if_inverse_plot_backwards=None,
        inverse=None,
        max_random_grid_offsets=None,
        max_random_real_offsets=None,
        mode_index=None,
        name=None,
        num_video_workers=None,
        partial_grid_shape=None,
        partial_real_shape=None,
        partial_real_position=(0.0,0.0,0.0),
        plot_dpi=None,
        plot_interpolation=None,
        plot=None,
        reduce_volume=None,
        switch=None,
        wave_characters=None,
        components=None,
        index=None
    ):
        kwargs = locals()
        kwargs.pop("self")
        if index:
            kwargs.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)
        # None-Werte löschen
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        obj = fdtdx.ModeOverlapDetector(**kwargs)
        self.real_position(obj=obj)

        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)
        return obj

    

    def create_phasor_detector(
        self, *,
        color=None,
        components=None,
        dtype=None,
        exact_interpolation=None,
        if_inverse_plot_backwards=None,
        inverse=None,
        max_random_grid_offsets=None,
        max_random_real_offsets=None,
        name=None,
        num_video_workers=None,
        partial_grid_shape=None,
        partial_real_shape=None,
        partial_real_position=(0.0,0.0,0.0),
        plot=None,
        plot_dpi=None,
        plot_interpolation=None,
        reduce_volume=None,
        switch=None,
        wave_characters=None,
        index=None
    ):
        kwargs = locals()
        kwargs.pop("self")
        if index:
            kwargs.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)

        # Entferne alle None-Werte
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        obj = fdtdx.PhasorDetector(**kwargs)
        self.real_position(obj=obj)
        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)
        return obj

    
    def create_poynting_flux_detector(
        self, *,
        color=None,
        direction=None,
        dtype=None,
        exact_interpolation=None,
        fixed_propagation_axis=None,
        if_inverse_plot_backwards=None,
        inverse=None,
        keep_all_components=None,
        max_random_grid_offsets=None,
        max_random_real_offsets=None,
        name=None,
        num_video_workers=None,
        partial_grid_shape=None,
        partial_real_shape=None,
        partial_real_position=(0.0,0.0,0.0),
        plot=None,
        plot_dpi=None,
        plot_interpolation=None,
        reduce_volume=None,
        switch=None,
        index=None
        ):
        kwargs = locals()
        kwargs.pop("self")
        if index:
            kwargs.pop("index")
            self.update_object_names(old=self.track_object_list[index].name, new=name)
        # Remove all None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        obj = fdtdx.PoyntingFluxDetector(**kwargs)
        self.real_position(obj=obj)
        if index:
            self.track_object_list.pop(index)
            self.track_object_list.insert(index, obj)
        else:
            self.track_object_list.append(obj)
        return obj
   
  
  
  # ============================================
  # DELETE FUNCTIONS
  # ============================================

    def delete_by_index(self, index: int):
        """Löscht ein Objekt anhand seines Index in der Liste."""
        if 0 <= index < len(self.track_object_list):

            self.delete_obj_constraints(self.track_object_list[index].name)
            del self.track_object_list[index]

            # Falls current auf ungültigen Index verweist → reset
            if self.current >= len(self.track_object_list):
                self.current = 0
            return True
        
        raise IndexError("Invalid index for delete operation.")

    def delete_by_object(self, obj_reference):
        for idx, obj in enumerate(self.track_object_list):
            if obj is obj_reference:
                del self.track_object_list[idx]

                if self.current >= len(self.track_object_list):
                    self.current = 0
                self.delete_obj_constraints(obj.name)
                return True
        return False
  
    def delete_by_object_name(self, name):
        for idx, obj in enumerate(self.track_object_list):
            if obj.name == name:
                del self.track_object_list[idx]

                if self.current >= len(self.track_object_list):
                    self.current = 0
                self.delete_obj_constraints(obj.name)
                return True
        return False

    # Configures by name and changes the color
    def change_color(self, color, object_name):
        if self.config(object_name) == -1:
            return -1
        self.track_object_list[self.current].color == color
        return 0
    def get_object_names(self):
        return (o.name for o in self.track_object_list)
    # returns a dict with objname as key and a tuple of 2 lists (sizes, pos)
    def get_all_dimensions(self, config):
        config = SimulationConfig(**config)
        #resolve_object_constraints returns 2 dicts, one with 3 slices per object for its dimenstions, and one with error messages per object
        objs, errors = fdtdx.resolve_object_constraints(objects=self.track_object_list, constraints=list(self.constraints.values()), config=config)
        if not all(e is None for e in errors.values()):
            raise Exception([k for k,v in errors.items() if v is not None])
        # Make 0,0,0 the center of the simulation volume in our scene
        vol = self.track_object_list[0].partial_real_shape
        for name, slices in objs.items():
            size = []
            pos = []
            for i,s in enumerate(slices):
                size.append((s[1] - s[0])*config.resolution)
                pos.append(((s[1] + s[0])/2)*config.resolution -(vol[i]/2))
            objs.update({name:(size, pos)})
        return objs

    
    def real_position(self, obj:SimulationObject):
        """This Function just hides that partial_real_position isnt used when resolving Constraints"""
        key = next(
            (k for k, v in self.constraints.items()
            if "hidden_" in k and v.object == obj.name),
            None
        )
        sim_vol = self.track_object_list[0]
        x,y,z = (None if a is None else (2*a/x) for a,x in zip(obj.partial_real_position, sim_vol.partial_real_shape))
        axes = tuple(val for cond, val in [(x, 0), (y, 1), (z, 2)] if cond is not None)
        if x is None and y is None and z is None:
            if key: self.constraints.pop(key)
            return
        if key is None:
            key = f"hidden_{self.uniqueName()}"
        self.constraints[key] = obj.place_relative_to(other=sim_vol, axes=axes, own_positions=tuple(0 for a in axes),other_positions=tuple(v for v in (x,y,z) if v is not None))
