import json
from pathlib import Path

import fdtdx


class Material:
    def __init__(self):
        # Load material_list.json from the same directory
        self.material_list = []  # List of materials in the form of: [Name(str), fdtdx Material, Editable(bool)]
        json_path = Path(__file__).parent / "material_list.json"
        with open(json_path, "r", encoding="utf-8") as f:
            self.material_list_json = json.load(f)

        for obj in self.material_list_json:
            if obj["__module__"] == "fdtdx.materials":
                self.material_list.append([obj["__name__"], self.create_material_from_list(obj), False])

    def create_material_from_list(self, obj):
        """Creates the corresponding material from a json dict obj"""
        material = fdtdx.Material(
            permeability=obj["permeability"],
            permittivity=obj["permittivity"],
            electric_conductivity=obj["electric_conductivity"],
            magnetic_conductivity=obj["magnetic_conductivity"],
        )
        return material

    def create_new_material(self, permability, permittivity, e_conductivity, m_conductivity, name="Unknown Material"):
        """Creates a new material with all given settings and appends it to the material list. None Values Will return standard values"""
        material = fdtdx.Material(
            permeability=permability,
            permittivity=permittivity,
            electric_conductivity=e_conductivity,
            magnetic_conductivity=m_conductivity,
        )
        self.material_list.append([name, material, True])

    def get_material_list(self):
        """returns the material list"""
        return self.material_list

    def remove_material(self, obj):
        """removes the given material from the list"""
        self.material_list.remove(obj)

    def get_name_from_material(self, material):  # returns name
        """returns the material list name for the given fdtdx.material"""
        for obj in self.material_list:
            if obj[1] == material:
                return obj[0]
        return "Material Not Found"

    def get_material_from_name(self, name):
        """returns the fdtdx.material with the given name from the list"""
        for obj in self.material_list:
            if obj[0] == name:
                return obj
        return -1

    def get_material_from_settings(
        self, permeability, permittivity, e_conductivity, m_conductivity, name="Unknown Material"
    ):
        """returns the material from material list that matches the settings. Creates a new one if it does not exist"""
        obj = self.material_exists_settings(
            permeability=permeability,
            permittivity=permittivity,
            e_conductivity=e_conductivity,
            m_conductivity=m_conductivity,
        )
        if obj != -1:
            return obj[1]
        self.create_new_material(
            permittivity=permittivity,
            permability=permeability,
            e_conductivity=e_conductivity,
            m_conductivity=m_conductivity,
            name=name,
        )
        return self.get_material_from_settings(permeability, permittivity, e_conductivity, m_conductivity)

    def material_exists_settings(self, permeability, permittivity, e_conductivity, m_conductivity):
        """checks if material exists with the given settings. Does not make a new one if not"""
        for obj in self.material_list:
            if (
                obj[1].permeability == permeability
                and obj[1].permittivity == permittivity
                and obj[1].electric_conductivity == e_conductivity
                and obj[1].magnetic_conductivity == m_conductivity
            ):
                return obj
        return -1

    def get_material_json(self, obj):
        """returns the given material in a json form"""
        return {
            "__module__": "fdtdx.materials",
            "__name__": obj[0],
            "electric_conductivity": obj[1].electric_conductivity,
            "magnetic_conductivity": obj[1].magnetic_conductivity,
            "permeability": obj[1].permeability,
            "permittivity": obj[1].permittivity,
        }
