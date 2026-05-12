import fdtdx
from nicegui import ui

from fdtdx_studio.ui.panels.object_config_panel import ObjectConfigPanel


class Material_panel(ObjectConfigPanel):
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

        # permittivity
        self.permittivityX = None
        self.permittivityY = None
        self.permittivityZ = None

        # permeability
        self.permeabilityX = None
        self.permeabilityY = None
        self.permeabilityZ = None

        # electric conductivity
        self.electric_conductivityX = None
        self.electric_conductivityY = None
        self.electric_conductivityZ = None

        # magnetic conductivity
        self.magnetic_conductivityX = None
        self.magnetic_conductivityY = None
        self.magnetic_conductivityZ = None

        # editable
        self.is_readonly = True

        # index in material list
        self.index = None

    def getMaterial(self, obj):
        """Update teh settings with the one from the material"""
        self.index = self.controller.model.material.material_list.index(obj)
        self.set_name(obj[0])
        self.set_permittivity(obj[1].permittivity)
        self.set_permeability(obj[1].permeability)
        self.set_electric_conductivity(obj[1].electric_conductivity)
        self.set_magnetic_conductivity(obj[1].magnetic_conductivity)
        self.set_read_only(obj[2])

    def checkButton(self, permittivity, permeability, e_conductivity, m_conductivity, name, label):
        """enables or disables the button based on inputs"""
        obj = self.controller.model.material.material_exists_settings(
            permeability=permeability,
            permittivity=permittivity,
            e_conductivity=e_conductivity,
            m_conductivity=m_conductivity,
        )
        if obj == self.controller.model.material.get_material_from_name(self.original_name):
            obj = -1
        if obj == -1:
            label.set_text("Changes applied")
            label._style("color:green")
            label.set_visibility(True)
            self.update_material(
                permittivity=permittivity,
                permeability=permeability,
                electric_conductivity=e_conductivity,
                magnetic_conductivity=m_conductivity,
                name=name,
            )
            self.getMaterial(self.controller.model.material.get_material_from_name(name=name))
        else:
            label.set_text("Material with the same settings already exists: " + obj[0])
            label._style("color: red")
            label.set_visibility(True)

    def render_into(self, panel):
        """Render the configuration UI inside the given panel (clears first)."""
        if panel is None:
            ui.notification("No panel found to render config panel into", color="red")
            return
        panel.clear()
        with panel:
            with ui.column().classes("w-full gap-2 p-2"):
                name = (
                    ui.input(value=self.name if isinstance(self.name, str) else "")
                    .classes("w-full")
                    .bind_enabled_from(self, "is_readonly", backward=lambda x: not x)
                )

                ui.label("Permittivity").style("font-size: 13px; font-weight: bold;")
                with ui.row().classes("w-full flex-nowrap gap-1"):
                    permittivityX = (
                        ui.number("x", value=self.permittivityX, min=0, step=0.1, validation=self._validate)
                        .classes("flex-1")
                        .props("dense")
                        .bind_enabled_from(self, "is_readonly", backward=lambda x: not x)
                    )
                    # permittivityY = ui.number('y', value= self.permittivityY, min= 0, step= 0.1, validation= self._validate).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)
                    # permittivityZ = ui.number('z', value= self.permittivityZ, min= 0, step= 0.1, validation= self._validate).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)

                ui.label("Permeability").style("font-size: 13px; font-weight: bold;")
                with ui.row().classes("w-full flex-nowrap gap-1"):
                    permeabilityX = (
                        ui.number("x", value=self.permeabilityX, min=0, step=0.1, validation=self._validate)
                        .classes("flex-1")
                        .props("dense")
                        .bind_enabled_from(self, "is_readonly", backward=lambda x: not x)
                    )
                    # permeabilityY = ui.number('y', value= self.permeabilityY, min= 0, step= 0.1, validation= self._validate).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)
                    # permeabilityZ = ui.number('z', value= self.permeabilityZ, min= 0, step= 0.1, validation= self._validate).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)

                ui.label("Electric Conductivity").style("font-size: 13px; font-weight: bold;")
                with ui.row().classes("w-full flex-nowrap gap-1"):
                    electric_conductivityX = (
                        ui.number(
                            "x",
                            value=self.electric_conductivityX,
                            min=0,
                            max=1.0,
                            step=0.1,
                            validation=self._validate_conductivity,
                        )
                        .classes("flex-1")
                        .props("dense")
                        .bind_enabled_from(self, "is_readonly", backward=lambda x: not x)
                    )
                    # electric_conductivityY = ui.number('y', value= self.electric_conductivityY, min= 0, max= 1.0, step= 0.1, validation= self._validate_conductivity).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)
                    # electric_conductivityZ = ui.number('z', value= self.electric_conductivityZ, min= 0, max= 1.0, step= 0.1, validation= self._validate_conductivity).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)

                ui.label("Magnetic Conductivity").style("font-size: 13px; font-weight: bold;")
                with ui.row().classes("w-full flex-nowrap gap-1"):
                    magnetic_conductivityX = (
                        ui.number(
                            "x",
                            value=self.magnetic_conductivityX,
                            min=0,
                            max=1.0,
                            step=0.1,
                            validation=self._validate_conductivity,
                        )
                        .classes("flex-1")
                        .props("dense")
                        .bind_enabled_from(self, "is_readonly", backward=lambda x: not x)
                    )
                    # magnetic_conductivityY = ui.number('y', value= self.magnetic_conductivityY, min= 0, max= 1.0, step= 0.1, validation= self._validate_conductivity).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)
                    # magnetic_conductivityZ = ui.number('z', value= self.magnetic_conductivityZ, min= 0, max= 1.0, step= 0.1, validation= self._validate_conductivity).classes('flex-1').props('dense').bind_enabled_from(self, 'is_readonly', backward=lambda x: not x)

                if not self.is_readonly:
                    # Button for changing in XYZ Values
                    # ui.button('Apply Changes',on_click= lambda: self.update_material(name.value, [permittivityX.value,permittivityY.value,permittivityZ.value],[permeabilityX.value,permeabilityY.value,permeabilityZ.value],[electric_conductivityX.value,electric_conductivityY.value,electric_conductivityZ.value],[magnetic_conductivityX.value,magnetic_conductivityY.value,magnetic_conductivityZ.value]))
                    # Button for Changing in Scalar Values
                    Error = ui.label().style("font-size:13px; color: red")
                    self.apply = ui.button(
                        "Apply",
                        on_click=lambda: self.checkButton(
                            name=name.value,
                            permittivity=permittivityX.value,
                            permeability=permeabilityX.value,
                            e_conductivity=electric_conductivityX.value,
                            m_conductivity=magnetic_conductivityX.value,
                            label=Error,
                        ),
                    )

    def _validate(self, value):
        """validates time and resolution inputs"""
        try:
            if self.isFloat(value):
                if value > 0:
                    self.apply.enable()
                    return None

                else:
                    self.apply.disable()
                    return "Number must be greater than zero"
            else:
                self.apply.disable()
                return "Input must be a number"
        except (TypeError, ValueError):
            self.apply.disable()
            return "Input must be a number"

    def _validate_conductivity(self, value):
        """validates conductivity inputs"""
        try:
            if self.isFloat(value):
                if value < 1 or value > 0:
                    self.apply.enable()
                    return None
                else:
                    self.apply.disable()
                    return "Number must be between 0 and 1"
            else:
                self.apply.disable()
                return "Input must be a number"
        except (TypeError, ValueError):
            self.apply.disable()
            return "Input must be a number"

    def update_material(self, name, permittivity, permeability, electric_conductivity, magnetic_conductivity):
        """updates the material with the set values"""
        material = fdtdx.Material(
            permittivity=permittivity,
            permeability=permeability,
            electric_conductivity=electric_conductivity,
            magnetic_conductivity=magnetic_conductivity,
        )
        self.controller.update_material([name, material, True], self.index)

    def set_permittivity(self, permittivity):
        """sets permittivity"""
        if isinstance(permittivity, (list, tuple)):
            self.permittivityX = permittivity[0]
            self.permittivityY = permittivity[1]
            self.permittivityZ = permittivity[2]
        else:
            self.permittivityX = permittivity
            self.permittivityY = permittivity
            self.permittivityZ = permittivity

    def set_permeability(self, permeability):
        if isinstance(permeability, (list, tuple)):
            self.permeabilityX = permeability[0]
            self.permeabilityY = permeability[1]
            self.permeabilityZ = permeability[2]
        else:
            self.permeabilityX = permeability
            self.permeabilityY = permeability
            self.permeabilityZ = permeability

    def set_electric_conductivity(self, electric_conductivity):
        if isinstance(electric_conductivity, (list, tuple)):
            self.electric_conductivityX = electric_conductivity[0]
            self.electric_conductivityY = electric_conductivity[1]
            self.electric_conductivityZ = electric_conductivity[2]
        else:
            self.electric_conductivityX = electric_conductivity
            self.electric_conductivityY = electric_conductivity
            self.electric_conductivityZ = electric_conductivity

    def set_magnetic_conductivity(self, magnetic_conductivity):
        if isinstance(magnetic_conductivity, (list, tuple)):
            self.magnetic_conductivityX = magnetic_conductivity[0]
            self.magnetic_conductivityY = magnetic_conductivity[1]
            self.magnetic_conductivityZ = magnetic_conductivity[2]
        else:
            self.magnetic_conductivityX = magnetic_conductivity
            self.magnetic_conductivityY = magnetic_conductivity
            self.magnetic_conductivityZ = magnetic_conductivity

    def set_read_only(self, editable):
        if editable:
            self.is_readonly = False
        else:
            self.is_readonly = True

    def set_name(self, name):
        self.name = name
        self.original_name = name

    def isFloat(self, element: "str") -> bool:
        """check if an input value is float"""
        try:
            float(element)
            return True
        except ValueError:
            return False
